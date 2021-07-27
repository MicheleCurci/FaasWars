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
The goal is to rotate the ship at 45 degrees to the x-axis. The angle can be +45° or -45° but obviously rotates to the nearest.

### Step #1

![image](https://user-images.githubusercontent.com/16895991/127230726-9132ea30-81f1-4ee0-b901-4d0466f0830d.png)

### Step #2

![image](https://user-images.githubusercontent.com/16895991/127230807-0953f5ce-2eb6-4a8b-8721-e1c22898424e.png)

### Step #3

![image](https://user-images.githubusercontent.com/16895991/127230865-525ff276-277b-4d42-8ece-7f6176b52c70.png)

### Step #4

![image](https://user-images.githubusercontent.com/16895991/127230929-54653968-7858-4d29-a1e8-4e220c6344f7.png)
