# Home Assistant Ring push patch

A local patch to the `firebase-messaging` library inside the `homeassistant` Docker container. It restores Ring
push events (Ding and Motion) to Home Assistant (HA). The container's filesystem is replaced whenever the container is
recreated, so the patch must be reapplied after every HA update. The upstream report is
[home-assistant/core#192723](https://github.com/home-assistant/core/issues/192723).

## Symptom

The Ring doorbell's **Ding** event entity (`event.front_door_ding`) stayed at *Unknown*, and the **Motion** event entity
had not updated since September 2026. Over the same period, the **Last activity** sensor kept updating 30 to 90 seconds
after each event. The automation that rings the Reolink Chime triggers on `event.front_door_ding`, so it never ran.

## Cause

The Ring integration gets polled data, such as Last activity, over HTTPS. It gets Ding and Motion only through push
messages, which Ring delivers through Google's Firebase Cloud Messaging (FCM) service. The `firebase-messaging` library
receives those messages and decrypts each one with two values sent alongside it: the sender's public key from the
`crypto-key` header, and the salt from the `encryption` header.

The library extracts those values by slicing a fixed number of characters off the start of each header (`[3:]` to strip
`dh=`, `[5:]` to strip `salt=`). The slicing works only while each header holds a single parameter. The Web Push
standard allows several, such as `dh=<key>;p256ecdsa=<key>`, and the evidence suggests that Ring's messages now carry
more than one, so everything after `dh=` reaches the Base64 decoder. The raw headers have not been logged, so their
exact contents are inferred, not observed. The values are also sent without trailing `=` padding, which the library's
decoder does not tolerate.

The first push message after startup therefore fails, and the library shuts its push client down altogether instead of
discarding that one message. The client stays down until HA restarts, and the next push message crashes it again.

The unpatched library logs this error:

```
ERROR (MainThread) [firebase_messaging.fcmpushclient] Unknown error: Incorrect padding, shutting down FcmPushClient.
  File ".../firebase_messaging/fcmpushclient.py", line 378, in _decrypt_raw_data
    crypto_key = urlsafe_b64decode(crypto_key_str.encode("ascii"))
binascii.Error: Incorrect padding
```

With only the padding fix applied, the same message fails one step later, because the decoded bytes are not a valid
key:

```
ERROR (MainThread) [firebase_messaging.fcmpushclient] Unknown error: Invalid EC key., shutting down FcmPushClient.
  File ".../http_ece/__init__.py", line 78, in derive_dh
ValueError: Invalid EC key.
```

Network access was ruled out: the container opens a TCP connection to `mtalk.google.com:5228` without error.

## Versions

| Component            | Version   |
|----------------------|-----------|
| Home Assistant       | 2026.11.2 |
| `firebase-messaging` | 0.4.5     |
| `ring-doorbell`      | 0.9.14    |
| Python in container  | 3.14      |

The fault was first diagnosed on HA 2026.6.3. Updating to 2026.11.2 did not fix it, because that release still bundles
`firebase-messaging` 0.4.5.

## Patch

The patch has two parts, and both are needed.

| Part           | File and location                                                     | Change                                                                                                                                                        |
|----------------|-----------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Padding        | `fcmpushclient.py`, `_decrypt_raw_data`                               | Appends `b"========"` to the crypto key and the salt before Base64 decoding, as the library already does for its stored keys. Python ignores excess padding. |
| Header parsing | `fcmpushclient.py`, `_handle_data_message`, plus a new `_header_param` function | Replaces the fixed-length slices with a lookup that splits each header on `;` and `,` and returns the `dh` or `salt` value by name.                           |

Run each command below on the Docker host as a single line. When a long command wrapped as it was pasted, the file path
was lost and `sed` failed with `sed: -i requires an argument`.

1. Apply the padding fix:

   ```bash
   docker exec homeassistant sed -i -e 's/(crypto_key_str.encode("ascii"))/(crypto_key_str.encode("ascii") + b"========")/' -e 's/(salt_str.encode("ascii"))/(salt_str.encode("ascii") + b"========")/' /usr/local/lib/python3.14/site-packages/firebase_messaging/fcmpushclient.py
   ```

2. Apply the header-parsing fix with `patch_fcm_headers.py`. The script is listed at the end of this file. It saves a
   backup as `fcmpushclient.py.orig`, refuses to run if the two lines it replaces do not match exactly, and makes no
   change if it has already been applied. A command that pipes a local file into `docker exec` must be run by hand,
   because the Claude Code sandbox blocks the Docker socket for it.

   ```bash
   docker exec -i homeassistant python3 - < patch_fcm_headers.py
   ```

   The script prints `patched: …/fcmpushclient.py`.

3. Confirm that the patched module loads and parses a header with two parameters:

   ```bash
   docker exec homeassistant python3 -c "import firebase_messaging.fcmpushclient as f; print(f._header_param('dh=abc;p256ecdsa=xyz', 'dh'), f._header_param('salt=s1', 'salt'))"
   ```

   The command prints `abc s1`.

4. Restart HA so that it loads the patched library:

   ```bash
   docker restart homeassistant
   ```

## Reapplying after an update

Run all four steps again after each HA update, or whenever the container is recreated. If a later image bundles a
different Python version, the `python3.14` part of the path in step 1 changes. The current path is shown by the
following command:

```bash
docker exec homeassistant python3 -c "import firebase_messaging, os; print(os.path.dirname(firebase_messaging.__file__))"
```

If the lines that the patch replaces no longer match, the upstream library has changed. Check the installed version and
the upstream issue before patching again:

```bash
docker exec homeassistant python3 -c "import importlib.metadata as m; print(m.version('firebase-messaging'))"
```

## Verification

After the restart on 20 November 2026 at 00:00, the HA log did not record any `FcmPushClient` error. Before the patch,
the client crashed within seconds of each restart, on a message that FCM had queued for it. A doorbell press at 00:05
changed **TW Door Ding** from *Unknown* to 00:05:17 and rang the Reolink Chime. The Ding entity updated three times
between 00:05:17 and 00:05:21. The **Motion** entity still showed 5 September 2026 at that point, but it
recorded motion events from 08:55 onwards on 20 November 2026, which confirms that motion pushes reach HA.

To check the result after reapplying the patch, press the doorbell: **TW Door Ding** changes to the time of the press
within a few seconds, and the Chime rings. If the push client fails again, the HA log contains the line
`shutting down FcmPushClient`. Successful pushes are not logged at the default log level, but the HA database records
each state change, and the following read-only query lists them:

```bash
docker exec homeassistant python3 -c "import sqlite3; c=sqlite3.connect('file:/config/home-assistant_v2.db?mode=ro', uri=True); q='select m.entity_id, s.state, datetime(s.last_updated_ts, \"unixepoch\") from states s join states_meta m on s.metadata_id=m.metadata_id where m.entity_id in (\"event.front_door_ding\",\"event.front_door_motion\") order by s.last_updated_ts desc limit 10'; [print(r) for r in c.execute(q)]"
```

## Related changes on 19 November 2026

- In Ring Control Center, five stale HA client registrations were removed: two `ring-doorbell:HomeAssistant` entries
  and three `Qemu Python` entries. The Ring integration in HA was then re-authenticated.
- The automation that rings the Reolink Chime uses a State trigger on `event.front_door_ding` with
  `not_from: unavailable`, and runs the `reolink.play_chime` action on Chime1. The automation is described in full
  under [Automations](#automations).

## Automations

Two automations in `/config/automations.yaml` act on the Ring events. Both were in place on 20 November 2026.

### Duplicate Ding events

Ring delivers each doorbell press to HA as several Ding events within about four seconds, although the Ring app records
a single Missed Ring. The HA recorder database shows the following updates to `event.front_door_ding` on
20 November 2026:

| Press | Ding entity updates                      | Chime plays before the fix |
|-------|------------------------------------------|----------------------------|
| 19:44 | 19:44:53.345, 19:44:53.723, 19:44:56.881 | 2                          |
| 20:25 | 20:26:05.165, 20:26:06.211, 20:26:09.053 | 3                          |

The `ring-doorbell` library treats a push message as an update to an earlier alert, and discards it, only when the
alert id and the alert timestamp both match. The duplicates pass that check, probably because their timestamps differ,
but the alert ids have not been logged, so the cause is unconfirmed.

An automation in `single` mode ignores a trigger only while a run is still in progress. The `reolink.play_chime` action
returns as soon as the hub accepts the command, without waiting for the tune to finish, so a run completes in under a
second and each later duplicate starts a new run. At 19:44 the second update arrived 0.4 seconds after the first,
while the first run was still in progress, which is why that press played the chime twice rather than three times.

### Front Door Ring - Set Reolink Hub

The automation plays the `originaltune` ringtone on Chime1 for each doorbell press, then toggles
`number.reolink_home_hub_message_volume` between 40 and 41. A 10-second `delay` as its last action keeps each run in
progress until the duplicate Ding events have arrived, so `mode: single` discards them, and `max_exceeded: silent` stops
HA from logging an *Already running* warning for each one. A second genuine press within 10 seconds of the first does
not play the chime.

```yaml
alias: Front Door Ring - Set Reolink Hub
triggers:
  - trigger: state
    entity_id:
      - event.front_door_ding
    not_from: unavailable
actions:
  - action: reolink.play_chime
    data:
      device_id:
        - 0d858487d587251ae9359ba3cc083ec8
      ringtone: originaltune
  - action: number.set_value
    target:
      entity_id: number.reolink_home_hub_message_volume
    data:
      value: >
        {{ 40 if states('number.reolink_home_hub_message_volume') | int != 40
        else 41 }}
  - delay: "00:00:10"
mode: single
max_exceeded: silent
```

### Front door – motion without a ring

The automation plays the `waybackhome` ringtone on Chime1 when someone approaches the door but does not press the
doorbell. The Ring app labels such an event *Person Detected*, but HA cannot make the same distinction: the Ring
integration's Motion event entity has the single event type `motion`, and the `ring-doorbell` library's alert does not
carry Ring's detection type. The automation therefore triggers on any motion event that Ring pushes to HA.

Each motion event starts a run, unless a Ding event occurred in the previous two minutes, because Ring sends motion
events alongside each doorbell press. The run waits 20 seconds for a Ding event and plays the chime only if none
arrives. On 20 November 2026 the first Ding came 5, 12 and 11 seconds after the first motion event of the presses at
09:46, 19:44 and 20:25, so the 20-second wait leaves about 8 seconds of margin. Raise the wait to 30 seconds if the
chime plays for visitors who did ring.

```yaml
alias: Front door – motion without a ring
triggers:
  - trigger: state
    entity_id: event.front_door_motion
    not_from: unavailable
conditions:
  - condition: template
    value_template: >
      {{ states('event.front_door_ding') in ['unknown', 'unavailable']
         or now() - as_datetime(states('event.front_door_ding')) > timedelta(minutes=2) }}
actions:
  - wait_for_trigger:
      - trigger: state
        entity_id: event.front_door_ding
        not_from: unavailable
    timeout: "00:00:20"
    continue_on_timeout: true
  - if:
      - condition: template
        value_template: "{{ wait.trigger is none }}"
    then:
      - action: number.set_value
        target:
          entity_id: number.reolink_home_hub_message_volume
        data:
          value: >
            {{ 40 if states('number.reolink_home_hub_message_volume') | int != 40
            else 41 }}
      - action: reolink.play_chime
        data:
          device_id:
            - 0d858487d587251ae9359ba3cc083ec8
          ringtone: waybackhome
mode: single
```

## Open work

- Post the findings on [home-assistant/core#192723](https://github.com/home-assistant/core/issues/192723), including
  the duplicate Ding events. Remove this patch once a fixed `firebase-messaging` ships in HA.
- Confirm whether the duplicate Ding events share an alert id. Before a doorbell press, run the `logger.set_level`
  action with `ring_doorbell: debug` and `firebase_messaging: debug`, then read the raw alerts in the HA log. The log
  level reverts at the next restart.
- To make the motion automation fire only for people, turn off the *Other Motion* alert type in the Ring app's Smart
  Alerts and keep *People* on. Whether Ring then stops sending the other motion events to HA has not been tested.
- Add `max_exceeded: silent` to the motion automation. Its runs are still logging an *Already running* warning for
  each repeated motion event.
- The HA log recorded `Unexpected exception during read` from `firebase_messaging.fcmpushclient` at 03:58 and 12:47 on
  20 November 2026, and a server Close message at 15:39. Ding and Motion events arrived after each one, so the push
  client recovered. Watch for a recurrence that does not recover.

## patch_fcm_headers.py

```python
"""Patch firebase_messaging to read dh= and salt= from multi-parameter push headers.

Runs inside the homeassistant container: docker exec -i homeassistant python3 - < patch_fcm_headers.py
"""

import shutil
from pathlib import Path

import firebase_messaging

TARGET = Path(firebase_messaging.__file__).parent / "fcmpushclient.py"
BACKUP = TARGET.with_suffix(".py.orig")

REPLACEMENTS = {
    'crypto_key = self._app_data_by_key(msg, "crypto-key")[3:]  # strip dh=':
        'crypto_key = _header_param(self._app_data_by_key(msg, "crypto-key"), "dh")',
    'salt = self._app_data_by_key(msg, "encryption")[5:]  # strip salt=':
        'salt = _header_param(self._app_data_by_key(msg, "encryption"), "salt")',
}

HELPER = '''

def _header_param(header: str, name: str) -> str:
    """Return one named value from a Crypto-Key or Encryption header."""
    for part in header.replace(",", ";").split(";"):
        key, _, value = part.strip().partition("=")
        if key == name:
            return value
    raise ValueError(f"{name}= not found in push header")
'''


def main() -> None:
    """Apply the header-parsing patch once, keeping a backup of the original file."""
    source = TARGET.read_text()
    if "def _header_param(" in source:
        print(f"already patched: {TARGET}")
        return
    for old in REPLACEMENTS:
        if source.count(old) != 1:
            raise SystemExit(f"expected exactly one match for: {old}")
    if not BACKUP.exists():
        shutil.copy2(TARGET, BACKUP)
    for old, new in REPLACEMENTS.items():
        source = source.replace(old, new)
    TARGET.write_text(source.rstrip("\n") + "\n" + HELPER)
    print(f"patched: {TARGET}")


main()
```
