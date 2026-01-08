# How to Update the Addon to Show ha_token Field

## Step 1: Copy Updated Files

Run the copy script:

```bash
cd /Users/georgehill/dev/home-assistant-NR
./copy-to-ha.sh
```

## Step 2: Uninstall the Old Addon

In Home Assistant:

1. Go to **Settings** → **Add-ons**
2. Click on **New Relic Metrics**
3. Click **Uninstall**
4. Confirm uninstall

⚠️ Don't worry - you can copy your configuration before uninstalling if you want to save it.

## Step 3: Reload Add-on Store

1. In the Add-on Store, click **⋮** (three dots, top right)
2. Click **Check for updates** or **Reload**

## Step 4: Install Fresh

1. Scroll to **Local add-ons** section
2. Click **New Relic Metrics**
3. Click **Install**
4. Wait for it to build (1-2 minutes)

## Step 5: Configure

Now when you click **Configuration**, you should see:

- **api_key**
- **account_id**
- **ha_token** ← This should now appear!
- **update_interval**
- **queries**

## Alternative: Force Rebuild (May Not Work)

If you don't want to uninstall, you can try:

1. Go to the addon page
2. Click **Rebuild**
3. Wait for rebuild
4. **Hard refresh** your browser (Ctrl+Shift+R or Cmd+Shift+R)
5. Check Configuration tab

If the field still doesn't appear, use the uninstall/reinstall method above.

## Quick Copy-Paste Configuration

Once the field appears, use this configuration:

```yaml
api_key: "NRAK-your-key-here"
account_id: "your-account-id"
ha_token: "PASTE_YOUR_TOKEN_HERE"
update_interval: 300
queries:
  - name: "test_query"
    nrql: "SELECT count(*) FROM Transaction SINCE 5 minutes ago"
    icon: "mdi:chart-line"
```

Remember to create the Home Assistant token first:
1. Click your username (bottom left)
2. Scroll to "Long-Lived Access Tokens"
3. Create Token → Copy it
