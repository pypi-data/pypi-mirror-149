pro gimage,gstruc,image,larr,barr,plot=plot

; This program creates a 2D total intensity
; image using gaussians for each line of sight
; spectrum
;
;  INPUT
;   gstruc   Structure of gaussian parameters
;
;  OUTPUT
;   image    2D image constructed from the gaussians
;   larr     Array of longitudes
;   barr     Array of latitudes
;
; Created by David Nidever April 2005

ngstruc = n_elements(gstruc)

if (n_params(0) eq 0) or (ngstruc eq 0) then begin
  print,'Syntax - gimage,gstruc,image,larr,barr'
  return
endif

; Making sure it's the right structure
if (n_tags(gstruc) eq 0) then begin
  print,'Something Wrong With The Structure'
  return
endif
tags = tag_names(gstruc)
if (n_elements(tags) ne 8) then begin
  print,'Wrong Structure Type'
  return
endif
comp = (tags eq ['MLON','MLAT','GLON','GLAT','RMS','NOISE','PAR','SIGPAR'])
if ((where(comp ne 1))(0) ne -1) then begin
  print,'Wrong Structure Type'
  return
end

lon0 = min(gstruc.glon)
lon1 = max(gstruc.glon)
lat0 = min(gstruc.glat)
lat1 = max(gstruc.glat)

nlon = (lon1-lon0)*2. + 1.
nlat = (lat1-lat0)*2. + 1.

larr = findgen(nlon)*0.5 + lon0
barr = findgen(nlat)*0.5 + lat0

image = fltarr(nlon,nlat)

; Looping through all the longitudes
for i=0,nlon-1 do begin
  tlon = larr(i)

  ; Looping through all the latitudes
  for j=0,nlat-1 do begin

    tlat = barr(j)
    ind = where(gstruc.glon eq tlon and gstruc.glat eq tlat, nind)

    ; Found some gaussians at this position
    if nind gt 0 then begin
      all = 0.
      for k=0,nind-1 do all = all + garea(gstruc(ind(k)).par)
      image(i,j) = all
    end

  end ; for j
end  ; for i

;stop

if keyword_set(plot) then display,image,larr,barr,/interp

end
