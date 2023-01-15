import pynecone as pc


config = pc.Config(
    app_name="your_reaction_time",
    db_url="sqlite:///pynecone.db",
    env=pc.Env.DEV,
)
