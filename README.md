
# HyperBot V3 — Admin Full (Safe)

Everything included: verification, tickets (open/close + transcripts + auto-move), moderation, utilities, welcome + DM, logs, anti-spam, invite blocker (gift links allowed), reaction-role buttons, giveaways, status rotator.

## Run locally
1) Rename `.env.example` -> `.env` (or edit `.env`) and paste your **DISCORD_TOKEN** only.
2) `pip install -r requirements.txt`
3) `python bot.py`

## Railway
- Start command is set via Procfile: `python bot.py`
- Add all variables from `.env` into Railway → Variables (Raw Editor is easiest).

## Discord Developer Portal (Required)
Enable **Privileged Gateway Intents** on your bot (Bot tab):
- Presence Intent: ON
- Server Members Intent: ON
- Message Content Intent: ON

Invite URL: In OAuth2 → URL Generator:
- Scopes: `bot` + `applications.commands`
- Permissions: `Administrator`
