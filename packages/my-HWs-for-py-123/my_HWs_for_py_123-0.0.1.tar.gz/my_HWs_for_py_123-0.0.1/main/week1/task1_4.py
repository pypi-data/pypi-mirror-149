def file_converter(byte_size: bytes):
    units_array = ["B", "KB", "MB", "GB"]
    for unit in units_array:
        try:
            if byte_size < 1024:
                return (f'File size (converted): {round(byte_size, 1)} {unit}')
                break
            elif byte_size / 1024 ** (len(units_array) - 1) >= 1024:  # Что значит это условие?
                return (f'File size (converted): {byte_size / 1024 ** (len(units_array) - 1)} {units_array[-1]}')
                break
            else:
                byte_size /= 1024
        except TypeError:
            return (f'Incorrect \'byte_size\' value type')


if __name__ == '__main__':
    print(file_converter(19))  # '19.0B'
    print(file_converter(12345))  # '12.1Kb'
    print(file_converter(1101947))  # '1.1Mb'
    print(file_converter(572090))  # '558.7Kb'
    print(file_converter(999999999999))  # '931.3Gb'
