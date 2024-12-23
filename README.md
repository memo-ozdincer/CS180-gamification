# CS180-gamification
The first project we've had to do for ESC180/CS180, which was a Python implementation of a logic game/life simulation.

# Life Gamification Simulator
**Due Date: September 29, 2024 3:00 PM**

## Project Overview
A Python-based simulator for an exercise gamification app that encourages users to exercise through a reward system of "stars", health points, and hedons (fun points). The simulator models user behavior and can be used to test various reward strategies.

## Features
- Tracks user's health points and hedons (fun points)
- Simulates three activities: running, carrying textbooks, and resting
- Implements a star reward system that affects user motivation
- Models user fatigue and interest levels
- Calculates optimal activities based on potential hedon gains

## Activity Rules
### Health Points
- Running: 3 points/minute (first 180 mins), 1 point/minute (after 180 mins)
- Carrying Textbooks: 2 points/minute
- Resting: 0 points/minute

### Hedons (Fun Points)
- Variable based on:
  - User fatigue status
  - Activity duration
  - Star rewards
  - Previous activity history

## Functions
- `initialize()`: Resets all tracking variables
- `perform_activity(activity, duration)`: Simulates an activity
- `offer_star(activity)`: Offers a motivational star
- `get_cur_hedons()`: Returns current hedon count
- `get_cur_health()`: Returns current health points
- `most_fun_activity_minute()`: Suggests optimal activity

## Usage Example
```python
initialize()
perform_activity("running", 30)
print(get_cur_hedons())  # -20
print(get_cur_health())  # 90
