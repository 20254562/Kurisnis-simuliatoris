# Kurisnis-simuliatorius 
A short and "simple" simulation for rolling in WH40K tabletop game

## Introdution
So the goal of this project was mostly a passion project to see how dice simulators (mostly "ADEPT ROLL") work and maybe try to make my own simulation so that I would not need to spent money on premium features (spoiler alert it didn't). So to run this program you need run file: entry.py either in cmd or powershell.
Using it is simple in my opinion. You are presented with with interface looking like this: <img width="1920" height="991" alt="40k Combat Simulator 2026-04-24 09_05_32" src="https://github.com/user-attachments/assets/5c5f063d-fe4a-4456-b0b6-13bcbcc10ece" /> 

!!Almost all input numbers must be a possitive whole number. 

On weapons' side you have "A" that represent number of attacks, "WS" - how high of the roll you need to succesfully hit (say you input '3' so that means a simulation will need to roll 3 or higher to succesfully hit) using six sided dice and must be between 2-6, it will not accept 1 or 7+, S - streagth of the weapon(will be covered later), AP - armour pnetration, impacks a defenders save characteristic,, D - damage that weapon does. 
Worth noting that you can input XD3+Y or XD6+Y in attacks or damage (X and Y need to be int type numbers e.g. D3, D6+1,D3+1 or 2D6+4).
You can save and load weapon/defender profiles.
Next you can designate the number the weapons in count, then click add/update, also you can save and load weapon/defender profiles. Once added to attackers roster the nunber of weapons can still be edited, however to change it's e.g. weapon skill, you will have to change it at top boxes and click add/update button 
<img width="470" height="178" alt="Ekrano kopija 2026-04-24 111641" src="https://github.com/user-attachments/assets/fd345587-01e6-4c30-8404-1f772414e101" />
Defender works simuliary, but you only need to input T-toughnes, W-wounds, Sv-save and Inv-invulnabrility save(if it has one, can be left as a blank) and how many models make up defenders profile. Next just click simulate and see the results.

