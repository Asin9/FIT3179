document.addEventListener('DOMContentLoaded', function () {
    const selectElement = document.getElementById('visualization-select');
    const vegaEmbedContainer = document.getElementById('vega-embed-container');
    let view;
  
    // Define file paths for Vega-Lite specifications
    const specificationPaths = {
      visualization1: 'js/interactive_scattplot.vg.json',
      visualization2: 'js/world_symbol.vg.json'
      // Add more file paths for other views if needed
    };
  
    // Function to update the Vega-Lite visualization based on the selected option
    function updateVisualization(selectedOption) {
      if (view) {
        view.finalize(); // Clean up the previous visualization
      }
  
      // Embed the selected Vega-Lite specification
      vegaEmbedContainer.innerHTML = ''; // Clear the container
      vegaEmbedContainer.style.display = 'block';
      
      // Load the Vega-Lite specification from the file
      fetch(specificationPaths[selectedOption])
        .then(response => response.json())
        .then(spec => vegaEmbed(vegaEmbedContainer, spec))
        .catch(console.error);
    }
  
    // Add an event listener to the dropdown to update the visualization
    selectElement.addEventListener('change', function () {
      const selectedOption = selectElement.value;
      updateVisualization(selectedOption);
    });
  
    // Initialize the visualization with the default option
    const defaultOption = selectElement.options[0].value;
    selectElement.value = defaultOption;
    updateVisualization(defaultOption);
  });
  