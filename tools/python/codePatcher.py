# Disable the digital_effect_BW mode by substituting pointer to color mode
#   into switch table. 
digital_effect_patch_list = {}
digital_effect_patch_list['Digital_Mode_Disable_BW'] = {}
digital_effect_patch_list['Digital_Mode_Disable_BW']['start_offset'] = 0x375e28
digital_effect_patch_list['Digital_Mode_Disable_BW']['change_from'] = bytes([0x74, 0x72, 0x06, 0x80])
digital_effect_patch_list['Digital_Mode_Disable_BW']['change_to']   = bytes([0xec, 0x6f, 0x06, 0x80])

# rewrite argument to IR_CUT routine
ir_cut_disable_config_patch_list = {}
ir_cut_disable_config_patch_list['IR_CUT_Disable_Config'] = {}
ir_cut_disable_config_patch_list['IR_CUT_Disable_Config']['start_offset'] = 0x00095b4
ir_cut_disable_config_patch_list['IR_CUT_Disable_Config']['change_from'] = bytes([0x21, 0x20, 0x00, 0x00])
ir_cut_disable_config_patch_list['IR_CUT_Disable_Config']['change_to']   = bytes([0x01, 0x00, 0x04, 0x24])

# rewrite argument to IR_CUT routine
ir_cut_disable_on_wake_patch_list = {}
ir_cut_disable_on_wake_patch_list['IR_CUT_Disable_On_Wake'] = {}
ir_cut_disable_on_wake_patch_list['IR_CUT_Disable_On_Wake']['start_offset'] = 0x0009554
ir_cut_disable_on_wake_patch_list['IR_CUT_Disable_On_Wake']['change_from'] = bytes([0x21, 0x20, 0x00, 0x00])
ir_cut_disable_on_wake_patch_list['IR_CUT_Disable_On_Wake']['change_to']   = bytes([0x01, 0x00, 0x04, 0x24])

# rewrite the call that sprintf()'s the string to the bottom of the ribbon
wbwl_custom_ribbon_patch_list = {}
wbwl_custom_ribbon_patch_list['WBWL_Custom_Ribbon']['start_offset'] = 0x000273a8
wbwl_custom_ribbon_patch_list['WBWL_Custom_Ribbon']['change_from'] = bytes([0xd5, 0x88, 0x0d, 0x0c])
wbwl_custom_ribbon_patch_list['WBWL_Custom_Ribbon']['change_to'] = bytes([0xee, 0x9c, 0x01, 0x0c])


class codePatcher:
    ''''
    A class to apply patches from a patch list to a given binary file
    patch list  contains:
	'start_offset' -- relative to the start of program memory (e.g. 0x80000000)
	'change_from'  -- an array of bytes we expect to find at the given offset
	'change_to'    -- an array of bytes we will replace what's there with
    ''''

    # A function to add manual patches to an internal list
    internal_patch_list = {}

    # A function to add patches from source comipled lineage to patch list
    def add_bytes_file_to_patch_list(self, directory, new_bytes_filename, old_bytes_filename, start_offset):
    ## Get the patch name from the local directory name
	(head, patch_name) = os.path.split(directory)
	print(f'info: add_bytes_to_patch_list -- creating patch named: {patch_name}')
	self.internal_patch_list[patch_name] = {}
	self.internal_patch_list[patch_name]['start_offset'] = start_offset
	new_bytes_filepath = os.path.join(directory, new_bytes_filename)
	old_bytes_filepath = os.path.join(directory, old_bytes_filename)
	with open(new_bytes_filepath, 'rb') as new_bytes_f:
	    with open(old_bytes_filepath, 'rb') as old_bytes_f:
		old_bytes = old_bytes_f.read()
		new_bytes = new_bytes_f.read()
		self.internal_patch_list[patch_name]['change_from'] = old_bytes
		self.internal_patch_list[patch_name]['change_to'] = new_bytes
		
	return

    def add_to_internal_patch_list(patch_list):
	self.internal_patch_list.append(patch_list)
	return
    
    def patch_binary (self, binary_filename):
	print(f'Debug: patch_code -- opening {binary_filename} for patching')
	with open(binary_filename, "rb+") as binary_f:
	    data = self.apply_patches(binary_f)
	return

    def apply_patches(self,  binary_f):
	error = False
	# first check all the patches are pointing to the right (matching) binary
	for patch in self.internal_patch_list.keys():
	    offset = self.internal_patch_list[patch]['start_offset']
	    binary_f.seek(offset)
	    from_length = len(self.internal_patch_list[patch]['change_from'])
	    to_length = len(self.internal_patch_list[patch]['change_to'])
	    if from_length < to_length:
		print(f'Error: apply_patches -- patch {patch} : from len {from_length} is greater than available to len {to_length}')
		error=True
	    if from_length != to_length:
		print(f'Info: apply_patches -- patch {patch} : from len {from_length} to not the same as to len {to_length} -- only changing to_length')

	    actual_data = binary_f.read(to_length)
            ## truncate expected data to to_length -- only compare what we're replacing
	    expected_data = self.internal_patch_list[patch]['change_from']
	    if expected_data[:to_length] != actual_data:
		print(f'Error: apply_patches -- patch {patch} : at {offset:06x} Expected {expected_data}; Actual {actual_data}')
		error=True
		
	if (error):
	    print("Errors -- aborting Patch")
	    return
        # Now time to actually apply patches
	for patch in self.internal_patch_list.keys():
	    offset = self.internal_patch_list[patch]['start_offset']
	    change_to_data = self.internal_patch_list[patch]['change_to']
	    print(f'Debug: apply_patches -- patching location {offset:06x} to {change_to_data}')
	    binary_f.seek(offset)
	    binary_f.write(change_to_data)
	    
	return
