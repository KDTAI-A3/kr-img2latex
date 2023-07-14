import shutil


def unzip_dataset(train_path: str, test_path: str):
  """
    Unzip all data files. The files will be locataed on 'train' and 'test' directory.

    Args:
        train_path (str): File path of train zip file. 
        test_path (str): File path of test zip file.

    Returns:
        None
  """
  train_extract_dir = './train'
  test_extract_dir = './test'
  archive_format = 'zip'

  shutil.unpack_archive(train_path, train_extract_dir, archive_format)
  shutil.unpack_archive(test_path, test_extract_dir, archive_format)


if __name__ == '__main__':
    train_zip_file = './train.zip'
    test_zip_file = './test.zip'
    unzip_dataset(train_zip_file, test_zip_file)