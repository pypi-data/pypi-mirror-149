pro gloadspec,cubefile,lon,lat,spec,v,glon,glat,npts=npts,noise=noise

; This programs loads the spectrum for GDRIVER.PRO
; LON is the longitude index of the datacube
; LAT is the latitude index of the datacube

undefine,spec,v,glon,glat

if n_elements(lon) eq 0 or n_elements(lat) eq 0 then begin
  print,'Syntax - gloadspec,lon,lat,spec,v0,glon,glat,npts=npts,noise=noise'
  return
endif

; The first time
DEFSYSV,'!gauss',exists=gauss_exists
if not gauss_exists then begin
  print,'LOADING DATACUBE from ',cubefile
  FITS_READ,cubefile,cube,head
  FITS_ARRAYS,head,xarr,yarr,zarr
  szcube = size(cube)

  ;; Which dimension is velocity
  veldim = -1
  if stregex(strtrim(sxpar(head,'ctype1'),2),'vel',/boolean,/fold_case) eq 1 or $
     stregex(strtrim(sxpar(head,'ctype1'),2),'vrad',/boolean,/fold_case) eq 1 then veldim=0
  if stregex(strtrim(sxpar(head,'ctype2'),2),'vel',/boolean,/fold_case) eq 1 or $
     stregex(strtrim(sxpar(head,'ctype2'),2),'vrad',/boolean,/fold_case) eq 1 then veldim=1
  if stregex(strtrim(sxpar(head,'ctype3'),2),'vel',/boolean,/fold_case) eq 1 or $
     stregex(strtrim(sxpar(head,'ctype3'),2),'vrad',/boolean,/fold_case) eq 1 then veldim=2  
  if veldim ge 0 then begin
    print,'Detected the velocity dimension as axis=',strtrim(veldim+1,2)
  endif else begin
    print,'Cannot determine velocity dimension from the header.  Assuming it is the last dimension'
    veldim = 2
  endelse
  
  ;; Assign arrays
  case veldim of
    0: begin
      v0 = xarr
      glon0 = yarr
      glat0 = zarr
    end
    1: begin
      glon0 = xarr
      v0 = yarr
      glat0 = zarr
    end
    2: begin
      glon0 = xarr
      glat0 = yarr
      v0 = zarr
    end
    else:
  endcase
  
  ;; Convert from m/s to km/s
  if stregex(strtrim(sxpar(head,'cunit'+strtrim(veldim+1,2)),2),'m/s',/boolean,/fold_case) eq 1 or max(v0) gt 5000 then begin
    print,'Converting m/s to km/s'
    v0 /= 1e3 
  endif

  ;; Flip velocity/spectrum so that velocity is increasing
  if v0[1]-v0[0] lt 0 then begin
    print,'Flipping velocity/spectrum so that velocity is increasing'
    v0 = reverse(v0)
    cube = reverse(cube,veldim+1,/overwrite)
  endif

  ;; flip velocity
  ;;cube = reverse(cube,3)
  ;;v0 = reverse(v0)
  ;; Flip longitude
  ;;cube = reverse(cube,2)
  ;;glon0 = reverse(glon0)

  ;; Get proper coordinates using the WCS in the header
  xx = lindgen(n_elements(glon0))#replicate(1L,n_elements(glat0))
  yy = replicate(1L,n_elements(glon0))#lindgen(n_elements(glat0))
  XYAD,head,xx,yy,glon2d,glat2d

  ; missing data are set to roughly -1.52
  ;bd = where(cube lt -1,nbd)
  ;cube[bd] = !values.f_nan

  DEFSYSV,'!gauss',{cube:cube,head:head,v:v0,glon2d:glon2d,glat2d:glat2d,veldim:veldim}

  undefine,cube,glon2d,glat2d

Endif

; Load the spectrum
glon = !gauss.glon2d[lon,lat]
glat = !gauss.glat2d[lon,lat]
v = !gauss.v
case !gauss.veldim of
0: spec = reform(!gauss.cube[*,lon,lat]) ; vel,lon,lat
1: spec = reform(!gauss.cube[lon,*,lat]) ; lon,vel,lat
2: spec = reform(!gauss.cube[lon,lat,*]) ; lon,lat,vel
else:
endcase

; Only want good points
gd = where(finite(spec) eq 1,ngd)
mingood = 10            ; minimum number of GOOD spectral points (not NAN)

; No spectrum at this position, skip
if ngd lt mingood then begin
  rms = 999999.
  noise = 999999.
  undefine,spec,v
  npts = 0
  return
end else begin
  spec = spec[gd]
  v = v[gd]
  npts = n_elements(v)
  hinoise,v,spec,noise  ; get the noise
endelse

;stop

end
