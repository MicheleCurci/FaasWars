![logo](https://user-images.githubusercontent.com/16895991/126682823-f993639d-0f96-45c0-8ced-7f1609b9278b.png)
# FaasWars

This is the script of **Cortex2**, the bot with which I participated and won two [Faas Wars finals in season 1](https://nimbella.com/blog/results-and-feedback-of-faas-wars-may-the-faas-be-with-you).

There is also the **Cortex** script which earned second place in February.

The two scripts have the same structure, they differ only slightly in the logic of some features.

## Logic & steps

The bot's goal is to reach the **battle position** by approaching the closest side edge. As soon as the battle begins, the bot follows **several steps** to reach the final position. This phase is the **most delicate** because the bot is more vulnerable.

### Step #0

![image](https://user-images.githubusercontent.com/16895991/127230551-3a76a6d2-ecda-4fda-ba8a-67085e435a12.png)

Since the initial position of the bot is random, the first step is to reach the correct angle of the ship.
The goal is to rotate the ship at 45 degrees to the x-axis. The angle can be +45° or -45° but obviously the ship rotates to the nearest.

### Step #1

![image](https://user-images.githubusercontent.com/16895991/127230726-9132ea30-81f1-4ee0-b901-4d0466f0830d.png)

In this phase the ship is simply moving in one direction, towards the side edge.
The phase ends as soon as the ship approaches the edge.

### Step #2

![image](https://user-images.githubusercontent.com/16895991/127230807-0953f5ce-2eb6-4a8b-8721-e1c22898424e.png)

In step number two the ship must rotate to align parallel to the side edge.

### Step #3

![image](https://user-images.githubusercontent.com/16895991/127230865-525ff276-277b-4d42-8ece-7f6176b52c70.png)

The bot is ready for battle. The ship will decide whether to start moving up or down based on any sightings of the opponent occurred in the previous steps.

### Step #4

![image](https://user-images.githubusercontent.com/16895991/127230929-54653968-7858-4d29-a1e8-4e220c6344f7.png)

**It's time to take action!**
The ship will move and fire relentlessly trying to stay aligned with the opposing ship on the y-axis.
