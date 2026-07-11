WELCOME_MESSAGE = (
    "Welcome to Personal Horoscope Bot!\\n\\n"
    "I'll help you create a personalized daily horoscope based on your birth data "
    "and astronomical calculations.\\n\\n"
    "To get started, use /register to create your profile."
)

REGISTRATION_COMPLETE = (
    "Registration complete!\\n\\n"
    "Name: {name}\\n"
    "Gender: {gender}\\n"
    "Birth date: {birth_date}\\n"
    "Birth city: {birth_city}\\n\\n"
    "Use /horoscope to get your daily horoscope!"
)

PROFILE_TEMPLATE = (
    "Your Profile:\\n\\n"
    "Name: {name}\\n"
    "Username: @{username}\\n"
    "Gender: {gender}\\n"
    "Birth date: {birth_date}\\n"
    "Birth time: {birth_time}\\n"
    "Birth city: {birth_city}\\n"
    "Timezone: {timezone}\\n"
    "Member since: {created_at}"
)

HOROSCOPE_TEMPLATE = "Daily Horoscope for {name}\\nDate: {date}\\n\\n{horoscope_text}"

ERROR_MESSAGE = "An error occurred. Please try again later."

ALREADY_REGISTERED = "You are already registered! Use /profile to see your profile."

NOT_REGISTERED = "You are not registered yet. Use /register to create your profile."
