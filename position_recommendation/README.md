# Alpha Vision Plus - position recommendation

## Overview
This directory, as part of the Alpha Vision + Capstone Project, contains scripts and notebooks facilitating the vectorization of chess board states and implementing a dual-agent system for analyzing and recommending chess positions.

## Project Structure
- **board_utils.py**: A library of functions for converting chess board states into vectors and processing game data.
- **semantic_agent.ipynb**: Notebook for parsing PGN files and converting them into FEN strings, utilizing semantic analysis.
- **dynamic_agent.ipynb**: Implements a Convolutional Neural Network (CNN) for learning dynamic evaluations of chess positions.
- **masters_database.ipynb**: Manages SQL queries and database interactions for storing and retrieving vectorized positions.
- **position_recommendation.ipynb**: Handles the feedback loop and updates the recommendation engine based on user interactions.

## Usage Instructions
1. **Vectorization and Database Setup**:
   - Use `masters_database.ipynb` to set up and configure your PostgreSQL database for storing chess positions.
   - Run `board_utils.py` to generate vector representations of chess positions for analysis.

2. **Training the CNN**:
   - Execute `dynamic_agent.ipynb` to train the neural network on your dataset. Modify parameters within the notebook as needed for your configuration.

3. **Analyzing Positions**:
   - Convert new game data into FEN format using `semantic_agent.ipynb`.
   - Analyze positions and handle user feedback through `position_recommendation.ipynb`.

4. **Running the System**:
   - Ensure your PostgreSQL database is accessible and properly configured as per instructions in `masters_database.ipynb`.
   - Follow the provided order, starting from data preparation in `semantic_agent.ipynb` to interaction management in `position_recommendation.ipynb`.

## Additional Notes
- Data we used are accessible through pydrive, please contact Jim Yang (jimy@umich.edu) for credentials.
- Testing the system with a subset of your data before full deployment is advisable to ensure proper configuration.
