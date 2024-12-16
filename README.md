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

demo Video :
https://youtu.be/DMuCgaxGTJM?si=LvITecFhKdY7CdRb

## Project design and implementation
UML diagram
link below:
https://lucid.app/lucidchart/8026c604-59e6-44bb-ba54-900068d5b19c/edit?viewport_loc=-1040%2C-253%2C2918%2C1181%2CHWEp-vi-RSFO&invitationId=inv_0b8f6436-8f9f-48b1-9dce-3a6e251faadc

## 1. `Paddle` Class

**Purpose**:  
- It represents the player.

**Interactions**:  
- **DodgeBall**: The `DodgeBall` class uses the `Paddle` object in the main game (1-to-1) to represent the player in the game. The position of the paddle is controlled by `PaddleMovement`.

---

## 2. `PaddleMovement` Class

**Purpose**:  
- It controls the paddle’s movement and listens for player input (such as arrow keys) to move the paddle left, right, up, or down. It also manages the "blink" ability, allowing the paddle to flash in a chosen direction when activated.

**Interactions**:  
- **DodgeBall**: The `PaddleMovement` class interacts with the `DodgeBall` class by updating the position of the paddle within the game.
- **Paddle**: The `PaddleMovement` class updates the `Paddle`'s position based on user input (arrow keys or blink commands).

---

## 3. `DodgeBall` Class

**Purpose**:  
- It combine all the classes and acts as the main game controller. It provides the interface for starting and ending the game to manage functionality and game flow.

**Interactions**:  
- **Ball**: The `DodgeBall` class uses **Ball** objects as obstacles that the player must dodge.
- **Paddle**: The `DodgeBall` class uses **Paddle** as the player’s character, which can interact with the ball when a collision occurs.
- **PaddleMovement**: The `DodgeBall` class uses `PaddleMovement` to control the paddle's movement.
- **Event**: The `DodgeBall` class schedules and processes events, like ball collisions, using the `Event` class.

---

## 4. `Ball` Class

**Purpose**:  
- The **Ball** class represents the ball that bounces off walls and the paddle. It has changing speed and size as the game progresses.

**Interactions**:  
- **Paddle**: The ball can collide with the paddle.
- **Event**: The **Ball** class is involved in events that trigger actions, such as collisions with the paddle or walls.

---

## 5. `Event` Class

**Purpose**:  
- The `Event` class represents various game events, such as ball-paddle, ball-wall, and ball-ball collisions. The class stores all information about the event.

**Interactions**:  
- **Ball / Paddle**: The `Event` class references the **Ball** or **Paddle** involved in the event. For example, when a ball hits the paddle, an event is triggered and processed.
- **DodgeBall**: The `DodgeBall` class schedules and processes `Event` objects to handle game interactions like ball movements, collisions, and scoring.
## Enhancements:

- I have improved the paddle's movement to be smoother by changing from tab-based movement to holding a key.
- I added a new feature where the paddle can "blink" to move quickly in a chosen direction.
- For the **Ball** class, I introduced stages, making the game progressively harder as time goes on.
- In the main class, I added interfaces for starting the game, displaying gameplay instructions, and showing a menu after the game ends.

## Bugs:

- It seems the hitbox for the paddle is not always accurate in certain situations.
- After pressing Restart, the default speed of the paddle is higher than it should be.

## Rating:
I would rate my project sophistication level at 90/100 
