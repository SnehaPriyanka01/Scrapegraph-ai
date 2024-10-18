import json
from scrapegraphai.graphs import SmartScraperGraph

# Define the configuration for the scraping pipeline
graph_config = {
    "llm": {
        "url": "https://ollama.dealwallet.com/",  # Ensure this URL is correct for your setup
        "model": "ollama/llama3"  # Updated to the proper format 'provider/model_name'
    },
    "verbose": True,
    "headless": True
}

# Create the SmartScraperGraph instance
smart_scraper_graph = SmartScraperGraph(
    prompt="List me all the projects with their descriptions.",
    source="https://perinim.github.io/projects",
    config=graph_config
)

# Run the pipeline
result = smart_scraper_graph.run()

# Print the result
print(json.dumps(result, indent=4))
