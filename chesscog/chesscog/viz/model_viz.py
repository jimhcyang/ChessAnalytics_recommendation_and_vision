import torch
from torchviz import make_dot

def find_first_conv2d_module(model):
    """
    Find the first Conv2d module in the model.

    Parameters:
    - model: The PyTorch model to search.

    Returns:
    - The first Conv2d module or None if not found.
    """
    for module in model.modules():
        if isinstance(module, torch.nn.Conv2d):
            return module
    return None

def visualize_model_torchviz(model, filename='model_visualization'):
    """
    Visualize a PyTorch model using torchviz, automatically inferring the input size.

    Parameters:
    - model: The PyTorch model to visualize.
    - filename: The filename to save the visualization.
    
    The function generates and saves a diagram of the model architecture.
    """
    model.eval()  # Set the model to evaluation mode

    # Attempt to find the first Conv2d layer to infer input_size
    first_conv = find_first_conv2d_module(model)
    if first_conv is None:
        raise ValueError("No Conv2d layer found in the model. Cannot infer input size.")

    # Assuming the typical color image with 3 channels, but you might need to adjust for your model
    input_channels = first_conv.in_channels
    input_size = (input_channels, 224, 224)  # You might want to adjust the spatial dimensions

    sample_input = torch.randn(1, *input_size)  # Create a sample input tensor
    if torch.cuda.is_available():
        model.cuda()
        sample_input = sample_input.cuda()

    output = model(sample_input)  # Perform a forward pass (just for tracing)

    # Generate visualization
    dot = make_dot(output, params=dict(list(model.named_parameters()) + [('input', sample_input)]))
    dot.render(filename, format='png')  # Save the diagram as a PNG file
    print(f"Model visualization saved to {filename}.png")

# Usage example: visualize_model_torchviz(your_model)
