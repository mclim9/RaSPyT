from iSocket import iSocket                 # Import socket module
import numpy as np
import timeit

# #############################################################################
# ## Code Begin
# #############################################################################
fileName = 'iSck_VSG_IQ_FromArray'
clock = 122.88e6                                                # Sampling Rate
IData = [0.1, 0.2, 0.3]
QData = [0.4, 0.5, 0.6]

# ## ASCII
scpi  = f':MMEM:DATA:UNPR "NVWFM://var//user//{fileName}.wv",#' # Ascii Cmd
numBytes = str(len(IData) * 4)                                  # Calculate bytes of IQ data
scpi  = scpi + str(len(numBytes)) + numBytes                    # Calculate length of iqsize string
# ## Binary
iqdata = np.vstack((IData, QData)).reshape((-1,), order='F')    # Interleave I & Q data
iqdata = iqdata * 32767                                         # scale to 7bit number
bits  = np.array(iqdata, dtype='>i2')                           # Convert to big-endian 2byte int
# ## ASCII + Binary
cmd   = bytes(scpi, 'utf-8') + bits.tostring()                  # Add ASCII + Bin

K2 = iSocket().open('192.168.58.115', 5025)
tick = timeit.default_timer()
K2.writeBin(cmd)
K2.write(f'SOUR1:BB:ARB:WAV:CLOC "/var/user/{fileName}.wv",{clock}') # Set Fs/Clk Rate
K2.write(f'BB:ARB:WAV:SEL "/var/user/{fileName}.wv"')                # Select Arb File
testtime = timeit.default_timer() - tick

samples = len(IData)
print(f'Error   : {K2.query(":SYST:ERR?")}')
print(f'File    : {fileName}')
print(f'Samples : {samples}')
print(f'Clock   : {clock}')
print(f'Duration: {samples / clock * 1000} msec')
print(f'Transfer: Binary Transfer')
print(f'')
print(f'NumBytes: {numBytes}')
print(f'Time    : {testtime:.3f} Sec')
print(f'Thrput  : {int(numBytes)/testtime/1e6:.3f} MB /sec')
