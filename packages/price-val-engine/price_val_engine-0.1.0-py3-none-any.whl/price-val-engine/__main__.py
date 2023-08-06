from engine.core import Engine

if __name__ == "__main__":
    
    engine = Engine(
        input_file_path="input.csv",
        output_file_path="output.csv"
    )
    engine.validate_all()
    engine.save()

