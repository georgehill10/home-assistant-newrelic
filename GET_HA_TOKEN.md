# How to Get a Home Assistant Long-Lived Access Token

The addon needs a Home Assistant long-lived access token to create sensors.

## Steps to Create Token

### 1. Open Your Profile

1. In Home Assistant, click on your **username** in the bottom left sidebar
2. This opens your user profile page

### 2. Scroll to Long-Lived Access Tokens

1. Scroll down to the **"Long-Lived Access Tokens"** section
2. You'll see any existing tokens listed here

### 3. Create New Token

1. Click **"Create Token"** button
2. Enter a name like: **"New Relic Metrics Addon"**
3. Click **"OK"**

### 4. Copy the Token

**IMPORTANT:** The token will be shown only once!

1. A popup will appear with your new token
2. **Copy the entire token** (it's very long, starts with "eyJ...")
3. Store it safely - you won't be able to see it again

### 5. Add to Addon Configuration

1. Go to **Settings** → **Add-ons** → **New Relic Metrics**
2. Click **Configuration** tab
3. Paste the token in the **ha_token** field:

```yaml
api_key: "NRAK-your-newrelic-key"
account_id: "your-account-id"
ha_token: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiI..."  # Your long token here
update_interval: 300
queries:
  - name: "test_query"
    nrql: "SELECT count(*) FROM Transaction SINCE 5 minutes ago"
```

4. Click **Save**
5. **Restart** the addon

## Security Notes

- This token has full access to your Home Assistant instance
- Keep it secret and secure
- Don't share it or commit it to git
- You can revoke the token at any time from your profile
- If the token is compromised, delete it and create a new one

## Troubleshooting

### Can't find "Long-Lived Access Tokens"?

- Make sure you're clicking on your username (not settings)
- Scroll down on the profile page
- The section is below your user information

### Token not working?

- Make sure you copied the entire token
- Check for extra spaces or line breaks
- The token should be very long (100+ characters)
- Try creating a new token

### Lost the token?

- You cannot recover a token once the popup is closed
- Delete the old token and create a new one
- Update the addon configuration with the new token

## Example Full Configuration

```yaml
api_key: "NRAK-XXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
account_id: "1234567"
ha_token: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJmYWU0ZTBjZTQzZjI0MTIzYmM1NDQ0NjM4ZmU5YjE4MCIsImlhdCI6MTY3NzY4MjEyMCwiZXhwIjoxOTkzMDQyMTIwfQ.VeryLongTokenStringHere"
update_interval: 300
queries:
  - name: "transaction_count"
    nrql: "SELECT count(*) FROM Transaction SINCE 5 minutes ago"
    icon: "mdi:counter"
```
