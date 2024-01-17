# BotManClient

## Client component of [BotManServer](https://github.com/Mahasvan/BotManServer)

### Installation

- Clone the repository
- Install requirements
    - ```shell
      pip3 install -r requirements.txt
      ```
- Fill in `config.json` with appropriate data

### Running the App

- ```shell
  python3 main.py
  ```

### Config Structure

```json
{
  "token": "Your Discord Token",
  "server-ip": "localhost",
  "server-port": 8000,
  "guild-ids": []
}
```
