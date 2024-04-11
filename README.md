# Face Recognition

Face Recognition is a project for recognizing faces using Python and various libraries.

## Installation

To run this project, you need to have PyCharm installed. Follow these steps to set up your environment:

1. Install the following plugins in PyCharm:
    - Wheel
    - CMake
    - firebase-admin
    
2. Install the following Python libraries using pip:
    - dlib (version 19.20.0)
    ```
    pip install dlib==19.20.0
    ```
    - cvzone
    ```
    pip install cvzone
    ```
    - face-recognition
    ```
    pip install face-recognition
    ```

## Usage

To run the project, follow these steps:

1. Open PyCharm and navigate to the project directory.

2. Run the following scripts in the specified order:
    - AddDataToDatabase.py
    ```
    python AddDataToDatabase.py
    ```
    - EncodeGenerator.py
    ```
    python EncodeGenerator.py
    ```
    - main.py
    ```
    python main.py
    ```

## Contributing

Contributions to this project are welcome. If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License

This project is licensed under the [License Name] - see the [LICENSE.md](LICENSE.md) file for details.
