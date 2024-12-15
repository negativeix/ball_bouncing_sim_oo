# DodgeBall

This project is about a dodgeball game where the player must avoid balls bouncing off the walls. The balls will progressively increase in speed, number, and randomly vary in size.

## Installation

clone repository
```bash
git init
git clone https://github.com/negativeix/ball_bouncing_sim_oo.git
```

start game
```bash
python run_ball.py
```

## Usage & Example
control
| **Key**  | **Action**          | **Type**        |  
|----------|---------------------|-----------------|  
| ←        | Move player left    | Hold-to-move    |  
| →        | Move player right   | Hold-to-move    |  
| ↑        | Move player up      | Hold-to-move    |  
| ↓        | Move player down    | Hold-to-move    |  
| Spacebar | Blink player forward| Tap             |  

interaction
The player's color changes to indicate their current state:  
| **Color**  | **State**                      |  
|------------|--------------------------------|  
| White      | Normal state                  |  
| Black      | Waiting for blink cooldown    |  
| Red        | Player has taken damage       |  

