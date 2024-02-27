Alpha Vision +
==============================

Chess board state detection and move recommendation system

Project Summary
------------
Our capstone project aims to create an end-to-end comprehensive chess analysis tool that integrates digital insights into over the board play in chess. The project's primary objective is to utilize Computer Vision (CV) technology to interpret 3-D images of chess boards, converting these into 2-D board states using Forsyth–Edwards Notation (FEN). 

Subsequently, we will process the position and provide the user with chess insights to better help them navigate the position as they are playing or analyzing. We plan to build two types of chess engine systems. 

The primary focus of the first system will be matching scanned board states with similar positions from a database of master games. The second system will be reinforcement learning based using AlphaZero algorithm. The project intends to bridge the gap between offline chess and online analysis resources, providing users with gameplan inspiration through recognition of chess positions and advanced game analysis, offering a powerful resource for both enthusiasts and serious chess players.

Datasets
------------
Chess Games

- [http://caissabase.co.uk/](http://caissabase.co.uk/)
- [https://theweekinchess.com/twic](https://theweekinchess.com/twic)
- [https://database.lichess.org/](https://theweekinchess.com/twic)

Computer Vision

- [https://www.kaggle.com/datasets/thefamousrat/synthetic-chess-board-images/data](https://theweekinchess.com/twic)
- [https://doi.org/10.4121/99b5c721-280b-450b-b058-b2900b69a90f.v2](https://theweekinchess.com/twic)
- [https://public.roboflow.com/object-detection/chess-full](https://theweekinchess.com/twic)
- [https://paperswithcode.com/dataset/dataset-of-rendered-chess-game-state-images](https://theweekinchess.com/twic)


Project Organization
------------

    ├── LICENSE
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── docs               <- A default Sphinx project; see sphinx-doc.org for details
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── src                <- Source code for use in this project.


--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
