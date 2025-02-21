# ForceSubBot

A Telegram bot that enforces subscription to specified channels before allowing users to upload videos to a database channel. Built with Python, Telebot, and MySQL.

## Features

*   Forces users to subscribe to multiple Telegram channels.
*   Uploads videos to a designated database channel.
*   Shares video links after subscription verification.
*   Admin-only `/stats` command for usage statistics.

## Prerequisites

*   Python 3.x
*   MySQL server
*   Telegram bot token from [@BotFather](https://t.me/BotFather)
*   Channel IDs for subscription and database channels

## Installation

1.  **Clone the Repository**

    ```bash
    git clone https://github.com/yourusername/ForceSubBot.git
    cd ForceSubBot
    ```

2.  **Install Dependencies**

    ```bash
    pip install -r requirements.txt
    ```

3.  **Set Up MySQL Database**

    ```sql
    CREATE DATABASE forcesub_bot;
    CREATE USER 'root'@'localhost' IDENTIFIED BY 'your_password'; -- Replace 'your_password' with your actual password
    GRANT ALL PRIVILEGES ON forcesub_bot.* TO 'root'@'localhost';
    FLUSH PRIVILEGES;
    ```

4.  **Configure the Bot**

    *   Rename `config.py.example` to `config.py`.
    *   Edit `config.py` with your own values:

        ```python
        BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"  # Replace with your bot token
        CHANNELS = [-1002340039535, -1002340039536]  # Replace with your channel IDs
        DB_CHANNEL = -1002340039537  # Replace with your database channel ID
        ADMIN_IDS = [123456789]  # Replace with your admin Telegram IDs
        DB_HOST = "localhost"
        DB_USER = "root"
        DB_PASSWORD = "your_password"  # Replace with your MySQL password
        DB_NAME = "forcesub_bot"
        ```

5.  **Run the Bot**

    ```bash
    python3 main.py
    ```

    To run in the background using `screen`:

    ```bash
    screen python3 main.py
    ```

    Press `Ctrl+A` then `D` to detach from the screen session.

## Usage

1.  Start the bot with `/start`.
2.  Join the required channels if prompted.
3.  Send a video to upload it to the database channel.
4.  Receive a link to view the uploaded video.
5.  Admins can use `/stats` to check usage statistics.

## How to Get Channel IDs

1.  Add the bot as an admin to the channel.
2.  Send a message in the channel and forward it to [@GetIDBot](https://t.me/GetIDBot).

## Notes

*   Ensure the bot is an admin in all channels (specified in `CHANNELS` and `DB_CHANNEL`).
*   For private channels, the generated links are only accessible to members.
*   To extend support to other file types, modify `content_types` in `main.py`.

## License

This project is licensed under the [MIT License](LICENSE). See the `LICENSE` file for details.

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

## Credits

Built by [yourusername](https://github.com/yourusername) with inspiration from various Telegram bot projects.
