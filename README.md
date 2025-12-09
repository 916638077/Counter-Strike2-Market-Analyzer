# Counter-Strike2-Market-Analyzer
This project calculates the price of a trade-up for the knife you want.

https://tuprd-my.sharepoint.com/:v:/g/personal/tuu65043_temple_edu/ERNT5owBALBFucuert_LtCcB9tlNzxnnFdBteF_IVJw_UQ?nav=eyJyZWZlcnJhbEluZm8iOnsicmVmZXJyYWxBcHAiOiJPbmVEcml2ZUZvckJ1c2luZXNzIiwicmVmZXJyYWxBcHBQbGF0Zm9ybSI6IldlYiIsInJlZmVycmFsTW9kZSI6InZpZXciLCJyZWZlcnJhbFZpZXciOiJNeUZpbGVzTGlua0NvcHkifX0&e=PE2qTh

After the CS2 update on October 23, 2025, there are now two ways to obtain a knife (the rarest item in the game). The first way is to pull it from a container (with a chance of less than 0.4%). The second way is to perform a trade-up using 5 Covert items. However, these items must come specifically from a collection that contains the desired knife.

For example, if a knife can be found in both the Gamma Case Collection and the Operation Hydra Collection, you can only use Covert items from those two collections. That is exactly what this program does:
it finds the collection(s) of the knife you want, looks up the Covert items from those collections, selects the cheapest one, and returns the total trade-up cost along with the possible profit.

#Challenges Faced

At first, I planned to get all the needed data directly from the Steam Market. However, you can’t retrieve the collection name from Steam Market listings. This completely broke my original approach and forced me to rethink the entire project.

I then tried using several third-party websites, but none of them would provide this data in a way that I needed. At that point, I honestly thought the project might not be possible.

After a lot of searching, I finally came across a public GitHub database that contained everything I needed for every skin in the game (over 13,000 items).

From there, the main challenge became learning how to properly work with a large external dataset and use it in my program. After putting everything together and testing it, the program worked exactly how I originally imagined it, and I’m really happy with the final result.

