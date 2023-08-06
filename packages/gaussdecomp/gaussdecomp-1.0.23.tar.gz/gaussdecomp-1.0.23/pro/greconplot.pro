pro greconplot,file,gstruc=gstruc,xr=xr,yr=yr,glon=glon,$
               glat=glat,mlon=mlon,mlat=mlat

; This program reconstructs what the gaussian
; analysis did

; getting structure
if not keyword_set(gstruc) then begin
  if not keyword_set(file) then rdgauss,gstruc
  restore,file
endif

orig_gstruc=gstruc
; Only using a selected region
if keyword_set(glon) and keyword_set(glat) then begin
  ind = where(gstruc.glon eq glon and gstruc.glat eq glat,nind)
  gstruc = gstruc(ind)
endif
if keyword_set(mlon) and keyword_set(mlat) then begin
  ind = where(gstruc.mlon eq mlon and gstruc.mlat eq mlat,nind)
  gstruc = gstruc(ind)
endif


;lat = -70.
lmin = min(gstruc.glon)
lmax = max(gstruc.glon)
bmin = min(gstruc.glat)
bmax = max(gstruc.glat)
nl = (lmax-lmin)*2.+1.
nb = (bmax-bmin)*2.+1.

for i=0,nb-1 do begin
  lat = i*0.5+bmin

  for j=0,nl-1 do begin
    lon = j*0.5+lmin
    rdhispec,lon,lat,spec,v

    ind = where(gstruc.glon eq lon and gstruc.glat eq lat,nind)

    if nind gt 0 then begin
      par = (gstruc(ind).par)(*)

      gplot,v,spec,par,xr=xr,yr=yr,$
            tit='Lon='+stringize(lon,ndec=1)+' Lat='+stringize(lat,ndec=1)

      print,'Lon=',strtrim(lon,2),' Lat=',strtrim(lat,2)
      printgpar,par

      stop

    end

  end
end

stop

gstruc = orig_gstruc

end
