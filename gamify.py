def initialize():
    """
    Sets all global variables to their initial states.
    """

    global cur_hedons, cur_health
    cur_hedons = 0
    cur_health = 0
    
    # Time tracking
    global cur_time
    cur_time = 0
    
    # Last activity and its duration
    global last_activity, last_activity_duration
    last_activity = None
    last_activity_duration = 0

    global last_star_activity, last_star_time
    last_star_time = -999
    last_star_activity = None

    global bored_with_stars, last_tiring_activity_end_time, last_tiring_activity_end_time
    bored_with_stars = False
    last_tiring_activity_end_time = -999

    global star_offers, running_session_time, textbook_session_time
    star_offers = []
    running_session_time = 0
    textbook_session_time = 0


def get_cur_hedons():
    """
    Returns the current number of hedons.
    """
    return cur_hedons


def get_cur_health():
    """
    Returns the current health points.
    """
    return cur_health


def offer_star(activity):
    """
    Offers a star for the specified activity.
    
    Args:
        activity (str): The activity for which the star is offered.
    """
    global last_star_time, bored_with_stars, star_offers, cur_time, last_star_activity

    if activity not in ["running", "textbooks"] or bored_with_stars:
        return

    # Remove outdated star offers
    star_offers = [t for t in star_offers if cur_time - t < 120]

    # Check if the user is bored with stars
    bored_with_stars = len(star_offers) >= 2

    # Offer a star if not bored
    if not bored_with_stars:
        last_star_time = cur_time
        last_star_activity = activity
        star_offers.append(cur_time)


def perform_activity(activity, duration):
    """
    Simulates performing an activity for a given duration.
    
    Args:
        activity (str): The activity being performed.
        duration (int): The duration of the activity in minutes.
    """
    global cur_health, cur_hedons, running_session_time, textbook_session_time
    global last_activity, cur_time, last_tiring_activity_end_time

    # Determine if user is tired
    is_tired = (cur_time - last_tiring_activity_end_time < 120)

    # Check if a star can be used
    star_used = star_can_be_taken(activity)

    # Reset session times if activity changes
    if activity != last_activity:
        running_session_time = textbook_session_time = 0

    # Perform the activity and update health and hedons
    if activity == "running":
        cur_health += calculate_health_running(duration)
        cur_hedons += calculate_hedons_running(duration, is_tired, star_used)
        running_session_time += duration
    elif activity == "textbooks":
        cur_health += calculate_health_textbooks(duration)
        cur_hedons += calculate_hedons_textbooks(duration, is_tired, star_used)
        textbook_session_time += duration
    elif activity == "resting":
        running_session_time = textbook_session_time = 0

    # Update time and last activity state
    cur_time += duration
    last_activity = activity
    if activity in ["running", "textbooks"]:
        last_tiring_activity_end_time = cur_time


def calculate_health_running(duration):
    """
    Calculates the health gained from running.

    Args:
        duration (int): The duration of running in minutes.

    Returns:
        int: Total health gained.
    """
    global running_session_time

    # Calculate time at higher and lower health gain rates
    time_at_3 = min(180 - running_session_time, duration)
    time_at_1 = duration - time_at_3

    # Calculate total health gain
    health_gain = (time_at_3 * 3) + (time_at_1 * 1)

    return health_gain


def calculate_hedons_running(duration, is_tired, star_used):
    """
    Calculates the hedons gained or lost from running.

    Args:
        duration (int): Duration of running in minutes.
        is_tired (bool): Whether the user is tired.
        star_used (bool): Whether a star was used.

    Returns:
        int: Total hedons gained or lost.
    """
    hedons = 0
    for minute in range(1, duration + 1):
        hedon_per_minute = -2 if is_tired else (2 if minute <= 10 else -2)
        if star_used and minute <= 10:
            hedon_per_minute += 3
        hedons += hedon_per_minute

    return hedons


def calculate_health_textbooks(duration):
    """
    Calculates the health gained from reading textbooks.

    Args:
        duration (int): The duration of reading in minutes.

    Returns:
        int: Total health gained.
    """
    return duration * 2


def calculate_hedons_textbooks(duration, is_tired, star_used):
    """
    Calculates the hedons gained or lost from reading textbooks.

    Args:
        duration (int): Duration of reading in minutes.
        is_tired (bool): Whether the user is tired.
        star_used (bool): Whether a star was used.

    Returns:
        int: Total hedons gained or lost.
    """
    hedons = 0
    for minute in range(1, duration + 1):
        hedon_per_minute = -2 if is_tired else (1 if minute <= 20 else -1)
        if star_used and minute <= 10:
            hedon_per_minute += 3
        hedons += hedon_per_minute

    return hedons


def star_can_be_taken(activity):
    """
    Determines if a star can be used for more hedons.

    Args:
        activity (str): The activity in question.

    Returns:
        bool: True if a star can be used, False otherwise.
    """
    global bored_with_stars, last_star_time, cur_time, last_star_activity
    return (not bored_with_stars and last_star_time == cur_time and last_star_activity == activity)


def most_fun_activity_minute():
    """
    Determines the most fun activity to perform for one minute.

    Returns:
        str: The most fun activity ("running", "textbooks", or "resting").
    """
    global cur_time, last_tiring_activity_end_time

    is_tired = (last_tiring_activity_end_time != -999 and 
                cur_time - last_tiring_activity_end_time < 120)

    running_hedons = calculate_hedons_running(1, is_tired, star_can_be_taken("running"))
    textbooks_hedons = calculate_hedons_textbooks(1, is_tired, star_can_be_taken("textbooks"))

    if running_hedons > textbooks_hedons and running_hedons > 0:
        return "running"
    elif textbooks_hedons > running_hedons and textbooks_hedons > 0:
        return "textbooks"
    return "resting"
