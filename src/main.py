from data_loader import load_and_clean
import analysis

df = load_and_clean("data/Pages_and_screens_Page_path_and_screen_class.csv")

df.to_csv("data/clean_for_powerbi.csv", index=False)

print(df.shape)

