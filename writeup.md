# What data are you using for your recommendation and why did you choose that data?

I'm using the favorite_genre and primary_language columns from the adventurer_metadata file and genre_id and language_code from the content_metadata file. I chose to use these because I believe that genre and language are the most important factors to consider when deciding what type of content an adventurer likes to view. If they mostly view content of a certain genre, then we can infer that they are interested in other content of the same genre. We can also assume that an adventurer would stay away from viewing content that isn't their primary language, because it could be hard for them to understand.

# Which adventurers does your recommender serve well? Why?

My recommender would work well on adventurers who generally watch a single

# Which adventurers does your recommender not serve well? Why?

- new users
- name unused features

# Why did you pick those three adventurers from the publisher you chose?

I picked these adventurers because they've viewed the most content out of all the adventurers. This gives me more information about the type of content they like to watch and makes it easier to predict the next content they will view.

# Why do you believe your recommender chose the content it did for those adventurers? Be specific.
