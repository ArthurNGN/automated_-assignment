import pandas as pd
import wikipedia

### WIP FILE, not used in pipeline

# Load the CSV file
df = pd.read_csv('results/df_tmdb.csv')

# Function to retrieve the plot section from a Wikipedia page
def get_wikipedia_plot(title):
    try:
        # Replace spaces with underscores
        formatted_title = title.replace(' ', '_')
        # Fetch the Wikipedia page
        page = wikipedia.page(formatted_title)
        # Find the Plot section
        content = page.content
        plot_start = content.lower().find('plot')
        if plot_start != -1:
            plot_end = content.lower().find('==', plot_start)
            if plot_end == -1:
                plot_end = len(content)
            plot_content = content[plot_start:plot_end].strip()
            return plot_content
        else:
            return "Plot section not found"
    except Exception as e:
        return f"Error: {e}"

# Create a new column in the dataframe for the plot
df['wikipedia_plot'] = df['title'].apply(get_wikipedia_plot)

# Save the updated dataframe
df.to_csv('results/wikipedia_plots.csv', index=False)
