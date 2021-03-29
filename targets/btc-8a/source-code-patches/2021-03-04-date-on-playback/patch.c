// 2021-02-27 Zak: 
//      C-code for an alternatve version of setDigitalEffect() found in 
//      baseline BTC-8A code.
//      This version only handles two modes -- 
//        - the default, standard color mode
//        - black and white mode (for use with IR)
//          (and for color camera, we may not even want to use that)
//      This eliminates a substantial amount of code vs. the original, 
//        space that I will eventually use for new functions and data 
//        structures. 
// 2021-03-03 Zak: 
//      Fixing up some data types

// Key learnings here:
//      all externs should be treated as the object themselves -- not as pointer
//      (even if they are pointers)
//      Function prototypes should reflect proper typing
//          at & to the function arguments to get the right compile-time types
//      e.g. should be
//          exter char s_some_string;
//             :
//          debug_printf(&s_some_string);
//       vs.
//          extern char * s_some_string;
//             :
//          debug_printf(s_some_string);
//       By default, setting the parameter in the link command file
//          sets the *address* (a hidden level of indirection)
//          with C always dereferencing that address to get the current
//          value. 

// 2021-03-04 Zak:
//        Pruned down the setDigitalEffect functiom so that it *only* does color photos
//        This to free up as much room as possible for functions aimed at displaying 
//        "LARGE PRINT" data and time during video playback
//            Pruned code consumes about 1,000 bytes (vs. 3600 in original)
//            Should be enough to do some interesting stuff



// Global Variables
extern char         BYTE_80439978;
extern char         BYTE_80439979;
extern unsigned int DAT_803e7298;
extern unsigned int DAT_8043997c;

extern char         s_Digital_Effect_BW_803abef7;

// External Functions
extern unsigned char get_DAT_80357b60_at_global_index(void);
extern void FUN_800d15ec(unsigned char);
extern void FUN_800c3d28(char, unsigned int, unsigned int, unsigned int);
extern void FUN_800d15a0(unsigned char);

extern void sp5kIqCfgSet(unsigned int, unsigned int);
extern void sp5kIqBlockEnable(char, unsigned int);
extern unsigned int debug_printf(char *);
extern void tty_printf(char *, unsigned int);

extern int lsprintf(char*, char*, unsigned int, unsigned int);

// Newly defined function(s)
void setDigitalEffect(unsigned int digital_effect, unsigned int brightness_hue, unsigned int brightness,
                      unsigned int param_4) {

  // Only do default digital effect -- which is color (no B&W)
  if (BYTE_80439978 != 0) {
    BYTE_80439979 = get_DAT_80357b60_at_global_index();
    FUN_800d15ec(BYTE_80439979);
    FUN_800c3d28(0x23, 0, 1, 0x22001);
    FUN_800d15a0(BYTE_80439979);
  }
  sp5kIqCfgSet(0x22001, 0);
  sp5kIqBlockEnable(0x2b, 0);
  sp5kIqBlockEnable(0x2c, 0);
  sp5kIqCfgSet(0x42000, 0);
  sp5kIqCfgSet(0x42001, 0);
  sp5kIqCfgSet(0x42002, 0);
  sp5kIqCfgSet(0x42003, 0);
  sp5kIqCfgSet(0x42004, 0);
  sp5kIqCfgSet(0x42005, 0);
  sp5kIqCfgSet(0x42006, 0);
  sp5kIqCfgSet(0x42019, 1);
  sp5kIqCfgSet(0x4201a, 0);
  sp5kIqCfgSet(0x4201b, 0);
  sp5kIqCfgSet(0x4201c, 0);
  sp5kIqCfgSet(0x4201d, 0);
  sp5kIqCfgSet(0x42007, 0);
  sp5kIqCfgSet(0x42008, 0);
  sp5kIqCfgSet(0x42009, 3);
  sp5kIqCfgSet(0x4200a, 0);
  sp5kIqCfgSet(0x4200b, 0);
  sp5kIqCfgSet(0x4200c, 7);
  sp5kIqCfgSet(0x4200d, 7);
  sp5kIqCfgSet(0x4200e, 0);
  sp5kIqCfgSet(0x4200f, 0);
  sp5kIqCfgSet(0x42010, 0);
  sp5kIqCfgSet(0x42011, 0x80);
  sp5kIqCfgSet(0x42012, 0x80);
  sp5kIqCfgSet(0x42013, 0x80);
  sp5kIqCfgSet(0x42014, 0);
  sp5kIqCfgSet(0x42015, 0);
  sp5kIqCfgSet(0x42016, 0);
  sp5kIqCfgSet(0x42017, 0);
  sp5kIqCfgSet(0x42018, 0xff);
  sp5kIqCfgSet(0x4201e, 0);
  sp5kIqCfgSet(0x4201f, 1);
  sp5kIqCfgSet(0x42020, 1);
  sp5kIqCfgSet(0x42021, (unsigned int)&DAT_803e7298);
  sp5kIqCfgSet(0x42022, 0);
  sp5kIqCfgSet(0x42023, 0);
  sp5kIqCfgSet(0x42024, 1);wbwl
  sp5kIqCfgSet(0x42025, 0);
  sp5kIqCfgSet(0x42026, 0);
  return;
}


// wbwl_custom_ribbon_sprintf
//     replaces a call to "sprintf" used to build string printed in the bottom right corner of 
//     photo/video review window
//  zak 2021-03-05: Created -- add placeholders for date and time (assuming we can get values for 
//     these from the media, somehow

void wbwl_custom_ribbon_sprintf(char *buffer, char * format, unsigned int current_media_index, unsigned int total_num_media) {
  lsprintf(buffer,"MM-DD-YYYY HH:MM  %d/%d" ,current_media_index, total_num_media);
}


Hand patches (after patch code) 
  - find the new function
  - rename the new function
  - identify the ASCII string

