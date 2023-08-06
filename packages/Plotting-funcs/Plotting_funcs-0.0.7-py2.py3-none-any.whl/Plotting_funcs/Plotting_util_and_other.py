import numpy as np
#from scipy.fftpack import fft,ifft
from numpy.fft import fft,ifft
import matplotlib.pyplot as plt
import pywt
import scipy
import scipy.signal
from scipy import signal
from Audio_proc_lib.audio_proc_functions import *
from nsgt import NSGT, LogScale, LinScale, MelScale, OctScale
#from constant_q_FB import create_filters
import time
import math
import librosa


def timeis(func):
    '''Decorator that reports the execution time.'''
  
    def wrap(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
          
        print(func.__name__, end-start)
        return result
    return wrap

#PLOTTING ROUTINES---------------------------------------------------------------------------------------


def plot_frequency_and_angle_response(impulse_resp):
    w, h = signal.freqz(impulse_resp)

    fig, ax1 = plt.subplots()
    ax1.set_title('Digital filter frequency response')

    ax1.plot(w, 20 * np.log10(abs(h)), 'b')

    ax1.set_ylabel('Amplitude [dB]', color='b')

    ax1.set_xlabel('Frequency [rad/sample]')

    ax2 = ax1.twinx()

    angles = np.unwrap(np.angle(h))

    ax2.plot(w, angles, 'g')

    ax2.set_ylabel('Angle (radians)', color='g')

    ax2.grid()

    ax2.axis('tight')



def plot_response(fs, w, h, title):

    "Utility function to plot response functions"

    fig = plt.figure()

    ax = fig.add_subplot(111)

    ax.plot(0.5*fs*w/np.pi, 20*np.log10(np.abs(h)))

    ax.set_ylim(-40, 5)

    ax.set_xlim(0, 0.5*fs)

    ax.grid(True)

    ax.set_xlabel('Frequency (Hz)')

    ax.set_ylabel('Gain (dB)')

    ax.set_title(title)
    


def plot_spectrogram(X,sr,y_scale="log"):
    librosa.display.specshow(librosa.amplitude_to_db(np.abs(X), ref=np.max),
                        sr=sr, x_axis='time', y_axis=y_scale)
    plt.colorbar(format='%+2.0f dB')
    #plt.title('Constant-Q power spectrum')
    plt.tight_layout()


def plot_cqt_custom(X,B=12,ksi_min=32.7):
    fig, ax = plt.subplots(1,1)
    #img = ax.imshow(librosa.amplitude_to_db(np.abs(X)),aspect="auto",origin="lower",extent=[0,X.shape[1],ksi_min,ksi_max])
    img = ax.imshow(librosa.amplitude_to_db(np.abs(X)),aspect="auto",origin="lower")
    #x_label_list = ['x1', 'x2', 'x3', 'x4']
    notes = librosa.note_to_hz(['C1', 'C2', 'C3', 'C4','C5','C6','C7'])
    inds = list( map( lambda ksi_m : int( np.floor(B*np.log2(ksi_m/ksi_min) + 1) - 1 ) , notes ) )
    y_label_list = ['C1', 'C2', 'C3', 'C4','C5','C6','C7']

    #ax.set_xticks([-0.75,-0.25,0.25,0.75])
    ax.set_yticks( inds )

    #ax.set_xticklabels(x_label_list)
    ax.set_yticklabels(y_label_list)

    fig.colorbar(img)





def plot_spectrogram_pseudo_RT(X):

    plt.ion() # Stop matplotlib windows from blocking

    # Setup figure, axis and initiate plot
    fig, ax = plt.subplots()
    xdata, ydata = [], []
    ln, = ax.plot([], [] )
    

    for col in X.T:
        #time.sleep(0.)


        # Get the new data
        xdata = np.arange(len(col))
        ydata = np.abs(col)


        # Reset the data in the plot
        ln.set_xdata(xdata)
        ln.set_ydata(ydata)

        # Rescale the axis so that the data can be seen in the plot
        # if you know the bounds of your data you could just set this once
        # so that the axis don't keep changing
        ax.relim()
        ax.autoscale_view()

        # Update the window
        fig.canvas.draw()
        fig.canvas.flush_events()




def plot_cqt_pseudo_RT(X,B,ksi_min):
    plt.ion() # Stop matplotlib windows from blocking

    # Setup figure, axis and initiate plot
    fig, ax = plt.subplots()
    xdata, ydata = [], []
    ln, = ax.plot([], [], 'ro-')

    notes = librosa.note_to_hz(['C1', 'C2', 'C3', 'C4','C5','C6','C7'])
    inds = list( map( lambda ksi_m : int( np.floor(B*np.log2(ksi_m/ksi_min) + 1) - 1 ) , notes ) )

    for col in X.T:
        #time.sleep(0.)


        # Get the new data
        xdata = np.arange(len(col))
        ydata = np.abs(col)


        # Reset the data in the plot
        ln.set_xdata(xdata)
        ln.set_ydata(ydata)


        #SET TICK LABELS AS NOTES
        #plt.xticks(inds)
        x_label_list = ['C1', 'C2', 'C3', 'C4','C5','C6','C7']
        ax.set_xticks( inds )
        ax.set_xticklabels(x_label_list)
        

        # Rescale the axis so that the data can be seen in the plot
        # if you know the bounds of your data you could just set this once
        # so that the axis don't keep changing
        ax.relim()
        ax.autoscale_view()

        # Update the window
        fig.canvas.draw()
        fig.canvas.flush_events()



        

def plot_magnitude_fft(yf,db,s,full=False):

    f = lambda s : "Normalized frequncy( x 2π rad/sample)" if s==1 else "frequncy(Hz)"

    N = len(yf)

    amplitude = abs(yf)
    #reference amplitude is the maximum so the range in 
    # 1) linear scale will be [0,1]
    # 2) db scale (db-FS) [-inf,0] (in reality its not inf but its practicaly inf) 
    #amplitude = amplitude/amplitude.max()

    #power = amplitude**2/N

    #Logic for the x axis plot:-------------
    xf = np.arange(0,N)
    freq_incr = s/N
    xf = xf*freq_incr    

    if not(full):
        #up to nyiquist frequancy
        xf = xf[:N//2]
        amplitude = amplitude[:N//2]
    #--------------------------------------


    if db:
       plt.plot( xf,20*np.log10(amplitude) )

       plt.xlabel( f(s) )
       plt.ylabel( "Amplitude(db scaled)" )
    else:
        plt.plot(xf,amplitude)
        plt.xlabel( f(s) )
        plt.ylabel( "Amplitude(linear scale)" )

    #x axis log 
    # ax = plt.gca()
    # ax.set_xscale('log')

    # plt.tick_params(axis='x', which='minor')
    # ax.xaxis.set_minor_formatter(FormatStrFormatter("%.1f"))





class interpolate:
    def __init__(self,cqt,Ls):
        from scipy.interpolate import interp1d
        self.intp = [interp1d(np.linspace(0, Ls, len(r)), r) for r in cqt]
    def __call__(self,x):
        try:
            len(x)
        except:
            return np.array([i(x) for i in self.intp])
        else:
            return np.array([[i(xi) for i in self.intp] for xi in x])

def plot_cqt(signal,c):
    Ls = len(signal)
    hf = -1

    x = np.linspace(0, Ls, 2000)
    grid = interpolate(map(np.abs, c[2:hf]), Ls)(x).T
    np.log10(grid, out=grid)
    grid *= 20
    pmax = np.percentile(grid, 99.99)
    plt.imshow(grid, aspect='auto', origin='lower', vmin=pmax-80, vmax=pmax)
    plt.colorbar()



def plot_TF_transform(c,transform,matrix_form,sr):

    if transform=="SCALE_FRAMES":

      if not(matrix_form):
        from scipy import interpolate
        c_matrix = []
        max_win_len = np.array( list( map( lambda x : len(x) , c ) ) ).max()
        for n in range(len(c)):
            N = len(c[n])
            fk = np.arange(N)*(22050/N)
            (x,y) = (fk,np.abs(c[n]))

            f = interpolate.interp1d(x, y)

            xnew = np.linspace(0, fk[N-1], max_win_len)
            ynew = f(xnew)
            c_matrix.append( ynew )  


        grid = np.array(c_matrix).T
        np.log10(grid, out=grid)
        grid *= 20
        pmax = np.percentile(grid, 99.99)
        plt.imshow(grid, cmap="inferno" ,aspect='auto', origin='lower', vmin=pmax-80, vmax=pmax,extent=[0,200,0,22050])

        plt.ylim(bottom=100)

        plt.yscale("log")

        loc = np.array([  100.,  1000., 10000.,22050.])
        labels = [ plt.Text(100.0, 0, '$\\mathdefault{100}$') , plt.Text(1000.0, 0, '$\\mathdefault{1000}$') , plt.Text(10000.0, 0, '$\\mathdefault{10000}$'), plt.Text(22050.0, 0, '$\\mathdefault{22050}$')  ]
        plt.yticks(loc,labels)    

        plt.ylim(top=22050)


        plt.colorbar()
        plt.ylabel("Hz (log scale)")

      else:
        plot_spectrogram(np.array(c).T,44100,"log")



    if transform=="NSGT_CQT":

      if not(matrix_form):
        plot_cqt(x,c)
      else:
        plot_spectrogram(c,44100,"cqt_notes")

    if transform=="STFT_custom":
      librosa.display.specshow(librosa.amplitude_to_db(np.abs(c), ref=np.max),
                    sr=sr, x_axis='time', y_axis="log")
      plt.colorbar(format='%+2.0f dB')
      #plt.title('Constant-Q power spectrum')
      plt.tight_layout()



#DCT4 transform-----------------------
def DCT4(samples):
    """samples : (1D Array) Input samples    
     to be transformed
     Returns:y (1D Array) Transformed  
    output samples
    """
    import numpy as np
    import scipy.fftpack as spfft
    N=len(samples)
    # Initialize
    samplesup=np.zeros(2*N)
    # Upsample signal:
    samplesup[1::2]=samples      
    y = spfft.dct(samplesup,type=3,
    norm='ortho')*np.sqrt(2)
    return y[0:N]

idct = lambda DCT_coefs : scipy.fftpack.idct(DCT_coefs,norm='ortho')
#--------------------------------------------------------------------------------------------------------------------


#CHANGE OF BASIS-CHANGE REPRESENTATION-FREQUENCY OR TIME-FREQUENCY REPRESENTAIONS  ( cqt,dft,stft ROUTINES)------------------------------------------------------------
def get_dft_mtx(signal_samples):

    dft_mtx = [  np.exp(-1j * ( ( 2*np.pi )/signal_samples )*k * np.arange( 0,signal_samples ) ) for k in range(signal_samples) ]

    dft_mtx = np.array(dft_mtx)

    #OR EQUIVALENTLY 
    #dft_mtx = fft(np.eye(signal_samples))

    return dft_mtx






def get_Synthesis_operator(g,a,M,L):

    N = L//a
    b = L//M

    g_pad = np.concatenate((g,np.zeros(L-len(g))))
    #center_around zero
    g_pad = translation_operator(g_pad,len(g)//2)

    #obtain a block D0
    D0=[]
    l = np.arange(L)
    for m in range(M):
        D0.append(g_pad*np.exp((2*np.pi*1j*m*b*l)/L))

    D0 = np.array(D0).T

    #D = np.kron(np.eye(N,dtype=int),D0)
    D = np.concatenate( (D0 , np.roll(D0.T,a).T ) ,axis=1 )
    for i in range(2,N):
        D = np.concatenate( (D , np.roll(D0.T,i*a).T ) ,axis=1 ) 

    
    return D









def instantiate_NSGT( x , fs , args_scale,args_fmin,args_fmax,args_bins,matrixform=0,reducedform=0,multithreading=False):

    scales = {'log':LogScale, 'lin':LinScale, 'mel':MelScale, 'oct':OctScale}
    try:
        scale = scales[args_scale]
    except KeyError:
        print('scale unknown')

    scl = scale(args_fmin, args_fmax, args_bins )

    nsgt = NSGT(scl, fs, len(x), real=1, matrixform=matrixform, reducedform=reducedform ,multithreading=multithreading)

    return nsgt

def sample_the_rows(X,pyramid_lvl,wavelet_type):
    #downsample_the_rows_of_a_matrix_using 1D pyramids ( 1))filtering ,2)downsampling )
    cA_tmp = X
    for i in range(pyramid_lvl):
        #going one level down
        tmp = list( map( lambda row: pywt.dwt(row, wavelet_type) , cA_tmp) )

        cA_tmp = np.array( list( map( lambda x: x[0] , tmp ) ) )
    
    return cA_tmp

def NSGT_forword(x,nsgt_obj,pyramid_lvl=3,wavelet_type='db2'):

    # forward transform 
    c = np.array( nsgt_obj.forward(x) )

    if pyramid_lvl:
        #Getting 3 levels ----------------------------------------------------------
        #Because of the redundency in time (small hop size) we perform a 1D pyramid on each of the rows (response of the filtering by a frequency) 
        # of level (pyramid_lvl)
        cA_tmp = c
        for i in range(pyramid_lvl):
            #going one level down
            tmp = list( map( lambda row: pywt.dwt(row, wavelet_type) , cA_tmp) )

            cA_tmp = np.array( list( map( lambda x: x[0] , tmp ) ) )
        
        c = cA_tmp
    

    return c



def NSGT_backward(c,nsgt_obj,pyramid_lvl=3,wavelet_type='db2'):

    if pyramid_lvl:
        #reconstruct the 3 levels---------------------------------
        #going back in the initial time resolution to reconstruct
        tmp_recon = c
        #note we can reconstruct in the lvl 1 (dont need to go up to 0)
        for i in range(pyramid_lvl):
            tmp_recon = np.array( list( map( lambda A,D: pywt.idwt(A,D, wavelet_type) , tmp_recon,np.zeros(tmp_recon.shape) ) ) )
        c = tmp_recon

    # inverse transform 
    s_r = nsgt_obj.backward(c)

    return s_r


def get_CQT(x ,hop_length = 256, bins_per_octave = 12 ,s=44100):

    C = librosa.cqt(y=x, sr=s, hop_length=hop_length, n_bins=7*bins_per_octave,

                    bins_per_octave=bins_per_octave)

    return C


#----------------------------------------------------------------------------------------------------------------------------




#PADD TO NEAREST POWER OF TWO---------------------------------------------------
def PadRight(arr):
    nextPower = NextPowerOfTwo(len(arr))
    deficit = int(math.pow(2, nextPower) - len(arr))

    arr = np.concatenate(( arr,np.zeros(deficit, dtype=arr.dtype)))
    return arr

def NextPowerOfTwo(number):
    # Returns next power of two following 'number'
    return math.ceil(math.log(number,2))

def PreviousPowerOfTwo(number):
    # Returns previous power of two 
    return int(math.pow( 2 , math.floor(math.log(number,2))-1 ))

def SliceToPrevious(arr):
    PreviousPower = PreviousPowerOfTwo(len(arr))
    arr = arr[:PreviousPower]
    return arr

#-------------------------------------------------------------------------------


def hz_to_index(ksi_m,B,ksi_min):
    #funtion to convert hz in analog frequency ksi_m to the corresponding index from 0 - 84 (for 12-tone equal temperament)
    return int( np.floor(B*np.log2(ksi_m/ksi_min) + 1) - 1 )

def hz_2_index(ksi_k,fs,signal_len):
    #function to convert hz in analog frequency ksi_k ->> index 
    return (ksi_k/fs)*signal_len




#filterbanks and multirate DSP---------------------------------------------


#HAAR FILTERBANK------------------------------------------------------
h = [1,1]/np.sqrt(2)
g = [1,-1]/np.sqrt(2)

def Harr_analysis(x,h,g):
    
    aprox_coefs = LTI_filtering(h,x)[::2]
    det_coefs = LTI_filtering(g,x)[::2]

    return aprox_coefs,det_coefs

def Haar_synthesis(aprox_coefs,det_coefs,h,g):
    n = len(aprox_coefs)
    out1 = np.zeros(2*n,dtype=x.dtype)
    out2 = out1.copy()

    #upsampling and filtering----------
    out1[::2] = aprox_coefs
    tmp1 = LTI_filtering(h,out1)

    out2[::2] = det_coefs
    tmp2 = LTI_filtering(g,out2)

    return tmp1+tmp2
#-----------------------------------------------------------




def DFT_analysis_bank(x,s):
#TOO SLOW DONT RUN for a big length signal
    N = len(x)
    h = np.ones(N)
    k = np.arange(N)
    w = k*2*np.pi/N
    n = np.arange(N)
    filterbank_out = np.array( list(map(lambda w : LTI_filtering( h*np.exp(-1j*w*(n/s)) , x ) , w ) ) )

    return filterbank_out



def refl(x):
    sign = lambda x : 1 if x>0 else -1
    n = len(X)
    m = np.linalg.norm(x)
    u = x

    if m!=0:
        b = x[0] + sign(x[0])*m[0]
        u[1:n] = u[1:n]/b

    
    u[1] = 1
    return u

def refl_row(A,u):
    b = -2/np.dot(u,u)
    w = b*np.dot(A.T,u)

    return A+np.outer(u,w)


if __name__ =='__main__':
    #load music
    x,s = load_music()
    
    #ANALYSE THE FRAME OPERATOR---------------
    
    #test(x,4096,1024)
    '''
    support = 512
    g = create_desiered_window("Blackman",support)
    a = 256
    M = 512
    L = 2048

    D = get_Synthesis_operator(g,a,M,L)
    S = np.dot(D,np.conj(D).T)
    plt.spy(np.abs(S),precision=1e-11)
    '''

    support = 32
    g = np.hamming(support)
    a = 16
    M = 32

    y = PadRight(x) 
    y=np.cos(np.pi*2*5*np.arange(256)/256)
    #y = np.concatenate((y,np.zeros(a)))
    X,frame_operator = gabor_analysis_faster(y,g,a,M)
    x_rec  = gabor_synthesis_faster(X,g,a,M,frame_operator)

    norm = lambda x: np.sqrt(np.sum(np.abs(np.square(x))))
    rec_err = norm(x_rec - y)/norm(y)
    print("Reconstruction error : %.16e \t  \n  " %(rec_err) )    


    N = 400
    L = 400
    Η = fir(N,L)


    ksi_min = 32.7
    ksi_max = 3951.07
    B=12
    ksi_s = s

    #basis, lengths = librosa.filters.constant_q(s, filter_scale=0.5)
    #resp = np.array( list( map( lambda h : LTI_filtering(h,x)  , basis )  ) )
    #downsampling the representetion (the rows)
    #resp_D = sample_the_rows(resp,6,'db2')
    #plt.imshow(librosa.amplitude_to_db(np.array(resp)),aspect="auto",origin="lower")

    #g = basis
    #f = PadRight(x)
    f = x
    gf = create_filters(ksi_min,ksi_max,ksi_s,B,len(f))

    Lk = list(map(lambda x : ((np.abs(fft(x))>1e-4)*1).sum() , gf ))
    ak = len(x)/np.array(Lk)
    #Lk_full = np.concatenate( ( np.array(Lk) , np.flip(np.array(Lk)) ) )
    #gf = fft(g,len(f))
    #gf = np.concatenate( (  gf ,  np.flip(gf) ) )
    #CONSTRUCTING THE ADDITIONAL FILTERS NEEDED-----

    ksi_k_1_index = np.ceil( hz_2_index(ksi_min,ksi_s,len(f)) ).astype(int)
    Lk = np.concatenate( ( np.array( [ (2*ksi_min*len(f) )/ksi_s ] ) ,np.array(Lk)  ) )
    platue_func = np.concatenate( ( np.ones( ksi_k_1_index ) , np.zeros(1) ) )
    platue_func = np.concatenate( ( platue_func , np.zeros( len(f) - 2*len(platue_func)) , np.flip(platue_func ) ) )
    gf = np.concatenate( ( np.array( [platue_func] ) , gf ) )

    '''
    #for the first filter
    ksi_k_1_index = np.ceil( hz_2_index(ksi_min,ksi_s,len(f)) ).astype(int)
    Lk_0 = 2*ksi_k_1_index

    #for the second filter
    ksi_s_index = np.ceil( hz_2_index(ksi_s,ksi_s,len(f)) ).astype(int)
    Lk_nyiquist_fr = np.ceil( ( (ksi_s-2*ksi_max)*len(f) )/ksi_s ).astype(int)


    Lk_full = np.concatenate( ( np.array( [ Lk_0 ] ) , np.array([Lk]) , np.array( [ Lk_nyiquist_fr ] ) ,np.flip(np.array(Lk)) ) )
    #Lk_full = np.concatenate( ( np.array( [ (2*ksi_min*len(f) )/ksi_s ] ) ,np.array(Lk) , np.flip(np.array(Lk)) ) )
    platue_func = np.concatenate( ( np.ones( ksi_k_1_index ) , np.zeros(1) ) )
    platue_func = np.concatenate( ( platue_func , np.zeros( len(f) - 2*len(platue_func)) , np.flip(platue_func ) ) )

    gf = np.concatenate( ( np.array( [platue_func] ) , gf ,  np.flip(gf) ) )
    '''

    c = NSG_analysis_test1(f,gf,Lk)
    f_rec = NSG_synthesis_test(c,gf,Lk)


    t = 1.0
    while(1.0+t>1.0):
        t/=2.0
    t*=2.0



    '''
    ksi_min = 32.7
    ksi_max = 3951.07
    B = 12
    scale = OctScale
    scl = scale(ksi_min, ksi_max , B )
    nsgt = NSGT(scl, s, len(x), real=1, matrixform=0, reducedform=0 ,multithreading=False)
    c = nsgt.forward(x)
    plot_cqt(x,c)

    # x = np.ones(100)
    # x[::2] = -1
    block_len = 512
    h = np.array([1,1])
    out = divide_and_conquer_toeplitz(h,x,block_len)
    LTI_filtering_toepliz(h,x)

    x = np.arange(3*10)
    Dn = get_downsampling_mtx(len(x) , 3)

    L = 2
    interpolation_filter(x,L)

    M = 8
    prefilter_and_downsampling(x,M)

    tmp = Harr_analysis(x,h,g)
    euclidian_dist( x,Haar_synthesis(tmp[0],tmp[1],h,g) )

    filt_num = 10
    '''

    '''
    #checking if ΦΦ* = Σφιφι*------------------------
    tmp = np.reshape( np.random.randn(16) , (4,4) )
    S = np.zeros((4,4))
    for i in range(4):
        S += np.outer(tmp[:,i],tmp[i])

    S1 = np.dot(tmp,tmp.T)
    #-----------------------

    #checking a pair of a 2D biorthogonal system
    tmp = np.array([[1,0],[np.sqrt(2)/2,np.sqrt(2)/2]])
    tmp_inv = np.linalg.pinv(tmp)
    origin = np.array([[0, 0, 0,0],[0, 0, 0,0]])
    data = np.concatenate(( tmp.T, tmp_inv  ))
    plt.quiver(*origin,  data[:,0], data[:,1] ,  color=['r','r','g','g'], scale=10)
    #-----------------------------------------
    '''
    #i(np.abs(x)>0)*1).sum() , basis ))

    basis, lengths = librosa.filters.constant_q(s, filter_scale=0.5)
    #Lk = list(map(lambda x : ((np.abs(fft(x))>1e-5)*1).sum() , basis ))
    Lk = list(map(lambda x : ((np.abs(fft(x))>1e-2)*1).sum() , basis ))
    ak = len(x)/np.array(Lk)

    def NSG_analysis(f,g,a):
        f = fft(f)
        k = 0  
        for gk in g:
        
            ck = np.sqrt(len(f)/a[k])*ifft(f*np.conj(gk))

    '''

    basis, lengths = librosa.filters.constant_q(s, filter_scale=0.5)
    resp = np.array( list( map( lambda h : LTI_filtering(h,x)  , basis )  ) )
    #downsampling the representetion (the rows)
    resp_D = sample_the_rows(resp,6,'db2')
    #plt.imshow(librosa.amplitude_to_db(np.array(resp)),aspect="auto",origin="lower")


    g = basis
    f = x

    Lk = list(map(lambda x : ((np.abs(fft(x))>1e-3)*1).sum() , g ))
    ak = len(x)/np.array(Lk)
    gf = fft(g,len(f))
    gf = np.concatenate( (gf,np.flip(gf)) )


    c = NSG_analysis_test(f,gf,ak)
    f_rec = NSG_synthesis_test(c,gf,ak)


    #CHECK FOR SUPPORT CONDITIONS
    #1)
    ksi_min = 32.7
    ksi_max = 3951.07
    B=12
    ksi_k = np.power(2,( (np.arange(B*7)+1)-1 )/B)*ksi_min
    ksi_k.sum() - ( (ksi_max-ksi_min)* ( np.power(2,1/B) - np.power(2,-(1/B)) ) )

    #2)
    (1/ak).sum()

    nsgt = instantiate_NSGT( x , s , "oct", ksi_min , ksi_max , 12 )
    X = NSGT_forword(x,nsgt,pyramid_lvl = 0)
    X = sample_the_rows(X,5,'db2')
    plot_cqt_pseudo_RT(X,B,ksi_min)

    plt.figure()

    plot_cqt_pseudo_RT(resp_D,B,ksi_min)



    plot_spectrogram_pseudo_RT(resp_D)


    '''
    #x = np.flip(np.arange(20))
    x = PadLeft(x)
    #amp = np.linalg.norm(x)
    #x = x/amp
    x1 = x.copy()
    #we want b a divizor of L
    b = 128
    M = len(x1)//b
    #x1 = periodization(x1,len(x)//b)
    x1 = periodization_v2(x1,len(x)//b)
    #tmp = fft(x1,M)
    tmp = fft(x1[:M])
    tmp1 = fft(x)[0:len(x):b]
    np.linalg.norm(tmp/np.linalg.norm(tmp)-tmp1/np.linalg.norm(tmp1))
    '''
    
    #ANALYSE THE FRAME OPERATOR---------------
    '''
    #test(x,4096,1024)
    
    support = 256
    g = create_desiered_window("Blackman",support)
    a = 256
    M = 512
    L = 2048

    D = get_Synthesis_operator(g,a,M,L)
    S = np.dot(D,np.conj(D).T)


    '''
    #-=----------------------------------------
    
    
    x = PadRight(x)
    #x = SliceToPrevious(x)


    support = 4096
    g = create_desiered_window("Blackman",support)
    a = 1024
    M = 4096

    X = gabor_analysis_faster(x,g,a,M)
    x_rec  = gabor_synthesis_faster(X,g,a,M)


    rec_err = np.linalg.norm( x[:len(x_rec)] - x_rec )
    #print("Reconstruction error : %.3e \t : %s \n time : %.4f "%(rec_err,end1-start1))


    #span the notes C1-B7 (85 fr chanels)------------------------------------------------------------------
    ksi_min = 32.7
    ksi_max = 3951.07
    B = 12
    M = np.ceil(B*np.log2(ksi_max/ksi_min)+1)
    
    m = np.arange(M)+1
    fr_range = ksi_min*(2**((m-1)/B))

    notes = librosa.hz_to_note(fr_range)

    nsgt = instantiate_NSGT( x , s , "oct", ksi_min , ksi_max , B )
    X = NSGT_forword(x,nsgt,pyramid_lvl = 0)


    
    a = 0
    '''


