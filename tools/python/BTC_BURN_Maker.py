import math
import os
import shutil

class BTC_BURN_Maker:
  default_all_files = ["SPHOST.header", "offset0", "offset1", "offset2.header", "offset2.A", "offset2.B", "offset3", "offset5", "offset6", "prometheus_trailer"]
  # Don't count the "prometheus" file when calculating file sizes
  default_size_files = ["SPHOST.header", "offset0", "offset1", "offset2.header", "offset2.A", "offset2.B", "offset3", "offset5", "offset6"]
  default_moved_files = ["offset0", "offset1", "offset2.header", "offset5", "offset6", "prometheus_trailer"]
  default_source_directory = "/content/drive/MyDrive/reversing/targets/browning-trail-cameras/btc-8e/manufacturer-firmware-images/"
  default_dest_directory = "/content/drive/MyDrive/reversing/targets/browning-trail-cameras/btc-8a/burn-images/2021-02-06-Baseline-from-eeprom/"
  default_eeprom_filename = "2020-01-20-BTC-8A-EEPROM-Image.bin"
  default_eeprom_dir = "/content/drive/MyDrive/reversing/targets/browning-trail-cameras/btc-8a/eeprom-images/"

  # update the component offsets based on new size information
  def update_sphost_sizes(self, header, size_map):
    root = header.ldata
    # update filesize
    filesize = 0;
    for filename in size_map.keys():
      filesize += size_map[filename]
    root['filesize'] = filesize;
    print(f'Updated filesize to 0x{filesize:04x}')
    # update offsets
    offset = size_map['SPHOST.header']; 
    for index in root['offset']:
      offset_name = 'offset' + chr(0x30 + index)
      if (index == 2):
        size = size_map['offset2.header'] + size_map['offset2.A'] + size_map['offset2.B']
      else:
        if (offset_name in size_map):  
          size = size_map[offset_name]
        else:
          size = 0;

      if (size == 0):
        root['offset'][index] = 0
        print(f'Updated {offset_name} to 0x0')
      else:
        root['offset'][index] = offset
        print(f'Updated {offset_name} to 0x{offset:04x}')
      offset += size
    return 

  # update_filesystem_size
  # Recalculate sizes of filesystems A & B stored in offset2
  def update_filesystem_size(self, header, size_map, index):
    size = size_map['offset2.' + index]
    bytes_per_sector = header.ldata['bytes_per_sector']
    if ((size % bytes_per_sector) != 0):
      print(f'Warning::update_file_system_sizes -- file system {index} size {size} not a multiple of sector size {bytes_per_sector}')
    sectors = math.ceil(size / bytes_per_sector)

    header.ldata['sectors'] = sectors;
    return

  # fprint_sphost_header
  # create a new SPHOST.header, print it to a file
  def fprint_sphost_header(self, header, binary_file, crc, endianness):
    root = header.ldata
    # write magic sequence
    address = 0;
    magic = root['magic']
    print(f'writing magic of {magic} to {address:04x}')
    binary_file.write(magic)
    # write file_length
    address += 16;
    filesize = root['filesize']
    print(f'writing filesize of 0x{filesize:04x} to 0x{address:04x}')
    binary_file.write(filesize.to_bytes(4, byteorder = 'little', signed = False))
    # write offsets
    for index in root['offset']:
      if (index == 0): continue   ## offset0 is assumed
      offset = root['offset'][index]
      print(f'writing offset{index} of 0x{offset:04x} to file address 0x{address:04x}')
      binary_file.write(offset.to_bytes(4, byteorder = 'little', signed = False))
      address += 4
    # write crc
    address = root['offset'][0] - 4
    print(f'writing crc of 0x{crc:04x} to 0x{address:04x}')
    binary_file.seek(root['offset'][0] - 4)
    binary_file.write(crc.to_bytes(4, byteorder = 'little', signed = False))
    return

  # utility function.  Does a bytewise xor of the contents of a byte buffer with
  #      argument
  #      (this to duplicate a step in the BURN file creation process 
  def xor_buffer(self, in_buffer, xor_value):
    out_buffer = bytearray(in_buffer)
    for i in range(len(in_buffer)):
      out_buffer[i] = in_buffer[i] ^ xor_value
    return(bytes(out_buffer))

  # fix_offset2_header
  # by this time, assume that offset2.A and .B offsets and sizes are correct
  # but we still need to reflect these sizes in the offset2_header file, otherwise
  # it will not load correctly. 
  def fix_offset2_header(self, offset2_header_filename, a_offset, a_size, b_offset, b_size):
    with open(offset2_header_filename, 'rb+') as f:
      # invert the contents of the file
      buffer = f.read(0x20)
      xored_buffer = self.xor_buffer(f.read(0x100), 0x7a)
  
      offset2header = Struct([
            ('header_string', '16s'),
            ('num_images', '1s'),
            ('header_padding', '15s'),
            ('drive_a_id_string', '20s'),
            ('drive_a_zeros', '92s'),
            ('drive_a_offset', 'I'),
            ('drive_a_size',  'I'),
            ('drive_a_padding', '8s'),
            ('drive_b_id_string', '20s'),
            ('drive_b_zeros', '92s'),
            ('drive_b_offset', 'I'),
            ('drive_b_size',  'I'),
            ('drive_b_padding', '8s')
            ], buffer + xored_buffer)
      offset2header.pretty_print()
      print('changing values')
      # change values
      offset2header.ldata['drive_a_offset'] = a_offset
      offset2header.ldata['drive_a_size'] = a_size
      offset2header.ldata['drive_b_offset'] = b_offset
      offset2header.ldata['drive_b_size'] = b_size
      print("---------------------")
      offset2header.pretty_print()
      print("---------------------")
      buffer = offset2header.pack_to_buffer()
      xored_buffer = self.xor_buffer(buffer[0x20:], 0x7a)
      f.seek(0)
      f.write(buffer[0:0x20])
      f.write(xored_buffer)
    return

  def copy_file_system_images(self, dest_directory, fs_directory):
    if not fs_directory:
      return
    else:
      src_filename = os.path.join(fs_directory, 'offset2.A')
      dest_filename = os.path.join(dest_directory, 'offset2.A')
      src_size = os.stat(src_filename).st_size
      dest_size = os.stat(dest_filename).st_size
      if (src_size != dest_size):
        print(f'Error: copy_file_system_images -- offset2.A src size {src_size} not equal to dest size {dest_size}')
        return
      with open(dest_filename, "rb") as dest_f:
        print(f'Debug: copy_file_system_image: Grabbing ICATCH FAT16 header from {dest_filename}')
        header_data = dest_f.read(512)

      print(f'Debug: copy_file_system_image: Copying {src_filename} to {dest_filename}')
      shutil.copy(src_filename, dest_directory)

      #with open(dest_filename, "rb+") as dest_f:
      #  print(f'Debug: copy_file_system_image: Writing ICATCH FAT16 header to new {dest_filename}')
      #  dest_f.write(header_data)

    return

  def combine_firmware(self, outfile='SPHOST.BRN', all_files=None, size_files=None, source_directory=None, dest_directory=None, 
                       dest_file=None, eeprom_source_directory=None, eeprom_source_file=None, fs_directory=None, patch_directory=None):
    '''Combine carved out chunks into a single firmware file
    Parameters
    ----------
    outfile : str
        File to save the firmware file to
    files : list(str)
        List of chunks to copy into firmware file. NOTE: The order is very
        important. 
    directory : str
        Directory where the chunks are located
    '''
    if not all_files:
      all_files = self.default_all_files

    if not size_files:
      size_files = self.default_size_files

    if not source_directory:
      source_directory = self.default_source_directory
    # Do nothing if directory or outfile are not valid
    if not os.path.isdir(source_directory):
      return

    if not dest_directory:
      dest_directory = self.default_dest_directory
    # Do nothing if directory or outfile are not valid
    if not os.path.isdir(dest_directory):
      return

    if not eeprom_source_directory:
      eeprom_source_directory = self.default_eeprom_dir

    if not eeprom_source_file:
      eeprom_source_file = self.default_eeprom_filename

    
    # Get the baselin burn image
    BRN_FILENAME = os.path.join(source_directory, "brnbtc80-K04290E.BRN")

    # Carve an image from the source_directory into the destination directory
    # Do this before extracting files from EEPROM so they overwrite
    carve_firmware(FILENAME=BRN_FILENAME, out_directory=dest_directory)

    # Get the EEPROM data (this will overwrite some files, above)
    eeprom_parser = BTC_EEPROM_Parser()
    eeprom_parser.update_all_eeprom_files(EEPROM_FILE=eeprom_source_file ,EEPROM_DIR=eeprom_source_directory, OFFSET_DIR=dest_directory)

    if patch_directory:
      # now -- time to patch the offset3 (application binary) file
      #patch_directory = '/content/drive/MyDrive/reversing/targets/browning-trail-cameras/btc-8a/source-code-patches/2021-02-28-set-digital-mode-rewrite'
      #patch_directory = '/content/drive/MyDrive/reversing/targets/browning-trail-cameras/btc-8a/source-code-patches/2021-03-04-date-on-playback'
      new_bytes_filename = 'patch.bytes'
      old_bytes_filename = 'existing_code.bytes'
      start_offset = 0x0066fb8

      patcher = codePatcher()
      patch_filename = os.path.join(dest_directory, 'offset3')
      patcher.add_wbwl_custom_ribbon_to_patch_list()
      patcher.add_bytes_file_to_patch_list(patch_directory, new_bytes_filename, old_bytes_filename, start_offset)
      patcher.patch_default(patch_filename)

    # now -- bring in a new file system image (if available)
    # zak -- save this for when we can rewrite FAT image
    #     -- for now, we're going to assume the right file system is on the EEPROM image
    #self.copy_file_system_images(dest_directory, fs_directory)


    SPHOST_FAT_INDEX = 2
    SPHOST_FAT_HEADER = 0x120
    # Read and parse all the headers SPHOST.BRN header
    with open(BRN_FILENAME, 'rb') as f:
        header = Struct([
            ('magic', '16s'),
            ('filesize', 'I'),
            ('offset', [
                (0, 0x200),
                (1, 'I'),
                (2, 'I'),
                (3, 'I'),
                (4, 'I'),
                (5, 'I'),
                (6, 'I')
                ]),
            ('crc', 'I')
            ], f.read(0x200))
        print("Baseline SPHOST Structure")
        print(header.ldata)
        header.pretty_print()
        print('-----------------------')
    # Loop over files to get their sizes
    size_map = {}
    total_size = 0;
    for filename in size_files:
      long_filename = os.path.join(dest_directory, filename)
      try:
        # Copy file contents to firmware file
        with open(long_filename, 'rb') as infile:
          size = os.path.getsize(long_filename)
          print(f'{filename} size is 0x{size:04x}')
          size_map[filename] = size
          total_size += size
      except FileNotFoundError:
        print(f'File {filename} not found.')
        break
    print(f'Total size is 0x{total_size:04x}')

    self.update_sphost_sizes(header, size_map)
    print("Updated SPHOST Structure")
    header.pretty_print()

    # build the SPHOST.header file
    filename = os.path.join(dest_directory, "SPHOST.header")
    # 2021-02-09 TODO: zak -- really calculate the CRC/Checksum
    crc = 0xdeadbeef
    
    with open(filename, 'wb') as header_file:
      self.fprint_sphost_header(header, header_file, crc, '<')

    # fix up the offset2.header file with actual sizes of the A and B images
    print(f'header.ldata[keys] = {header.ldata.keys()}')
    filename = os.path.join(dest_directory, "offset2.header")
    a_size = size_map['offset2.A']
    a_offset = header.ldata['offset'][2] + size_map['offset2.header']
    b_size = size_map['offset2.B']
    b_offset = a_offset + a_size
    self.fix_offset2_header(filename, a_offset, a_size, b_offset, b_size)


    # Combine files into a bundle
    brn_file = os.path.join(dest_directory, dest_file)
    combine_firmware(outfile=brn_file, files=self.default_all_files, directory=dest_directory)
  
    print('Done!')      
