# def main():
#     print("Hello from medical-ocr-extraction!")


# if __name__ == "__main__":
#     main()


if __name__ == "__main__":
    from src.ocr.extractor import extract

    data = extract('./src/resources/pd_1 (1).pdf', 'patient_details')
    print(data)
    