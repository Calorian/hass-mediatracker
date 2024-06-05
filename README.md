# MediaTracker JSON to HASS Sensor

## 1. Overview

The `MediaTracker` custom component for Home Assistant creates a sensor that fetches data from [Bonukai's MediaTracker API](https://github.com/bonukai/MediaTracker). The sensor state shows the number of upcoming events, and additional attributes provide detailed information about each event.

This sensor can then be used to feed a lovelace card. By default the component attributes work 'out-of-the-box' with the [Upcoming Media Card](https://github.com/custom-cards/upcoming-media-card) complete with poster and banner art.

## 2. Installation

1. **Download the Component**: 
   - Place the `media_tracker` folder in your `custom_components` directory within your Home Assistant configuration directory.

2. **Configure Home Assistant**:
   - Add the following configuration to your `configuration.yaml` file:
     ```yaml
     media_tracker:
         name: "Your Sensor Name"
         host: "your.api.host"
         port: your_api_port
         token: "your_api_token"
         days: number_of_days_to_track
         ssl: true_or_false
         json_only: true_or_false
     ```

3. **Restart Home Assistant**:
   - Restart Home Assistant to apply the new configuration and load the custom component.

## 3. Configuration

### Configuration Variables

- `name` (Optional): Custom name for the sensor. *Default = MediaTracker upcoming*
- `host` (Optional): Host or IP of your MediaTracker instance. *Default = localhost*
- `port` (Optional): Port of your MediaTracker instance. *Default = 7481*
- `token` (Required): Mediatracker authentication token for the API.
- `days` (Optional): The number of days to look ahead for upcoming media events. *Default = 7*
- `ssl` (Optional): Set to true if the API uses SSL (HTTPS). *Default = false*
- `json_only` (Optional): Set to true if you only want JSON output.. *Default = false*

## 4. Version History

* 0.2
    * Added 'JSON_ONLY' setting for those not using Upcoming media card.
* 0.1
    * Initial Release

## 5. Coming soon...

 - Extra sensors for MediaTracker lists (Watchlist etc.)
 - What to watch? - Grab a random next episode from the watchlist.

## 6. Support

For support and updates, please refer to [GitHub repository](https://github.com/calorian/hass-mediatracker) for this custom component or the [Home Assistant Community Forum](https://community.home-assistant.io/)

## 7. Support My Work
[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/calorian)

If you enjoy using this custom component and want to support my work, why not buy me a coffee? Your appreciation keeps me energized and motivated to continue improving and adding new features!
