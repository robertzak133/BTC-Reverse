g_offset_path = "/content/drive/MyDrive/reversing/targets/browning-trail-cameras/btc-8a/burn-images/2021-02-06-Baseline-from-eeprom/"
g_eeprom_path = "/content/drive/MyDrive/reversing/targets/browning-trail-cameras/btc-8a/eeprom-images/"
g_eeprom_filename = "2020-01-20-BTC-8A-EEPROM-Image-White-Flash-Color-Only-IR-Filter.bin"

class BTC_EEPROM_Parser:
  offset6_filename = "offset6"
  offset3_filename = "offset3"
  offset2a_filename = "offset2.A"
  offset2b_filename = "offset2.B"
  offset1_filename = "offset1"

  g_dram_par_offset = 0x100
  g_dram_par_length = 0x36a
  g_app_binary_offset = 0x303000
  g_app_binary_length = 0x425200
  g_a_fs_offset = 0x3000
  a_fs_length = 0x00
  g_b_fs_offset = 0x283000
  b_fs_length = 0x00
  c_fs_length = 0x00
  g_offset1_A_size_offset = 0x74   # Offset for {A, B, C, Sizes}


  g_a_struct_header = {}
  g_b_struct_header = {}

  def get_fat_size(self, eeprom_file, eeprom_file_offset, index):
    eeprom_file.seek(eeprom_file_offset)
    fatXXhdr = Struct([
            ('jump_instruction', '3B'),
            ('oem', '8s'),
            ('bytes_per_sector', 'H'),
            ('sectors_per_cluster','1B'),
            ('reserved_clusters','H'),
            ('num_fats','1B'),
            ('root_entries', 'H'),
            ('sectors', 'H'),
            ('media_type', '1B'),
            ('sectors_per_fat', 'H'),
            ('sectors_per_track', 'H'),
            ('num_heads', 'H'),
            ('hidden_sectors', 'I'),
            ('large_sectors', 'I'),
            ('physical_disk_number', '1B'),
            ('current_head', '1B'),
            ('signature', '1B'),
            ('volume_serial_number', 'I'),
            ('volume_label', '11s'),
            ('system_id', '8s')
            ], eeprom_file.read(0x60))
    fatXXsize = fatXXhdr.ldata['bytes_per_sector'] * fatXXhdr.ldata['sectors']
    fatXXhdr.pretty_print()
    if (index == 'A'):
      self.g_a_struct_header = fatXXhdr
    else:
      self.g_b_struct_header = fatXXhdr

    return(fatXXsize)

  def extract_offset6(self, EEPROM_FILE=g_eeprom_filename, EEPROM_DIR=g_eeprom_path, OFFSET_DIR=g_offset_path):
    print("Extracting Offset 6")
    with open(EEPROM_DIR + EEPROM_FILE, 'rb') as eeprom_file:
      with open(OFFSET_DIR + self.offset6_filename, 'wb') as offset6_file:
        eeprom_file.seek(self.g_dram_par_offset)
        data = eeprom_file.read(self.g_dram_par_length)
        offset6_file.write(data)
    return

  def extract_offset3(self, EEPROM_FILE=g_eeprom_filename, EEPROM_DIR=g_eeprom_path, OFFSET_DIR=g_offset_path):
    print("Extracting Offset 3")
    with open(EEPROM_DIR + EEPROM_FILE, 'rb') as eeprom_file:
      with open(OFFSET_DIR + self.offset3_filename, 'wb') as offset3_file:
        eeprom_file.seek(self.g_app_binary_offset)
        data = eeprom_file.read(self.g_app_binary_length)
        length = len(data)
        print(f'DEBUG::extract_offset_3: length of binary is 0x{length:06x}')
        offset3_file.write(data)
  

  def extract_offset2(self,EEPROM_FILE=g_eeprom_filename, EEPROM_DIR=g_eeprom_path, OFFSET_DIR=g_offset_path):
    print("Extracting Offset 2")
    with open(EEPROM_DIR + EEPROM_FILE, 'rb') as eeprom_file:
      with open(OFFSET_DIR + self.offset2a_filename, 'wb') as offset2a_file:
        self.a_fs_length = self.get_fat_size(eeprom_file, self.g_a_fs_offset, 'A')
        eeprom_file.seek(self.g_a_fs_offset)
        data = eeprom_file.read(self.a_fs_length)
        offset2a_file.write(data)
      with open(OFFSET_DIR + self.offset2b_filename, 'wb') as offset2b_file:
        self.b_fs_length = self.get_fat_size(eeprom_file, self.g_b_fs_offset, 'B')
        eeprom_file.seek(self.g_b_fs_offset)
        data = eeprom_file.read(self.b_fs_length)
        offset2b_file.write(data)
    return

  # Offset1 has a couple of references to file system sizes which we 
  #         need to fill in
  def modify_offset1(self, OFFSET_DIR=g_offset_path):
    print("Modifyng Offset 1")
    with open(OFFSET_DIR + self.offset1_filename, 'rb+') as offset1_file:
      offset1_file.seek(self.g_offset1_A_size_offset)
      offset1_file.write(self.a_fs_length.to_bytes(4, byteorder = 'little', signed = False))
      offset1_file.write(self.b_fs_length.to_bytes(4, byteorder = 'little', signed = False))
      offset1_file.write(self.c_fs_length.to_bytes(4, byteorder = 'little', signed = False))
    return

  # One stop shop -- update all the offset files that have data structures contained in the EEPROM image
  def update_all_eeprom_files (self, EEPROM_FILE=g_eeprom_filename, EEPROM_DIR=g_eeprom_path, OFFSET_DIR=g_offset_path):
    self.extract_offset6(EEPROM_FILE, EEPROM_DIR, OFFSET_DIR)
    self.extract_offset3(EEPROM_FILE, EEPROM_DIR, OFFSET_DIR)
    self.extract_offset2(EEPROM_FILE, EEPROM_DIR, OFFSET_DIR)
    self.modify_offset1(OFFSET_DIR)
    return
