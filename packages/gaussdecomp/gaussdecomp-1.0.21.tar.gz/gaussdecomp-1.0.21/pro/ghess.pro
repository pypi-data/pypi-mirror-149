pro ghess,gstr,xname,yname,zname,im,color=color,nx=nx,ny=ny,dx=dx,dy=dy,$
          xtit=xtit,ytit=ytit,tit=tit,log=log,interpolate=interpolate,$
          noplot=noplot,save=save,file=file,xrange=xrange,yrange=yrange,$
          stp=stp,cut=cut,top=top,total=total,bot=bot,norm=norm,$
          nocolorbar=nocolorbar,spread=spread,position=position,$
          onlyim=onlyim,noerase=noerase,charsize=charsize,$
          avg=avg,minhue=minhue,maxhue=maxhue,minbright=minbright,$
          maxbright=maxbright, saturation=saturation, xflip=xflip,$
          yflip=yflip,year=year,ctool=ctool,xout=xout,yout=yout,$
          posim=posim,poscol=poscol,thick=thick,charthick=charthick,$
          framecolor=framecolor,background_color=background_color,$
          twocut=twocut,threecut=threecut,colcharsize=colcharsize,$
          invert=invert,center=center,xarr=xarr,yarr=yarr,xlog=xlog,$
          ylog=ylog,maximum=maximum,sqroot=sqroot,column=column,$
          xsize=xsize,ysize=ysize,out_posim=out_posim,out_poscol=out_poscol,$
          ztop=ztop,zbot=zbot,wbot=wbot,colthick=colthick,colformat=form,$
          coldivisions=coldivisions,xtickformat=xtickformat,ytickformat=ytickformat,$
          xtickname=xtickname,xtickv=xtickv,ytickname=ytickname,$
          ytickv=ytickv,xticks=xticks,yticks=yticks,xminor=xminor,yminor=yminor,$
          rescale=rescale,radeg=radeg

;+
;
; This program makes a "Hess"-like diagram for a structure of Gaussians
;
;  INPUTS
;   gstr        Structure of gaussians
;   xname       Name of x-axis variable. Either 'ht','cen','sig','area','lon','lat'
;   yname       Name of y-axis variable. Either 'ht','cen','sig','area','lon','lat'
;   cut         A cut made in the data that can be made with the IDL
;                where statement.  This should be a string such as 'cen gt 5.0'.
;   /color      Plot in color
;   nx          Number of bins in x-axis.  Either set the # of bins or interval, not both
;   ny          Number of bins in y-axis
;   dx          Interval in x-axis.  Either set the # of bins or interval, not both
;   dy          Interval in y-axis
;   xtit        Title for x-axis on plot
;   ytit        Title for y-axis on plot
;   tit         Overall plot title
;   /log        Plot the logarithm
;   /xlog       Plot the x-axis on a logarithmic scale
;   /ylog       Plot the y-axis on a logarithmic scale
;   /interp     Interpolate between the points
;   /noplot     Don't plot anything
;   /save       Save the plot to a poscript file
;   file        Name of postscript file to save the plot to
;   xrange      X-axis plot range
;   yrange      Y-axis plot range
;   /stp        Stop at the end of the program
;   top         The largest value to plot
;   bot         The lowest value to plot
;   /total      Show total intensity instead of # of gaussians in each bin
;   /norm       If /total divide the intensity by the number of positions
;                in the bin
;   /spread     Spread out the intensity of a gaussian and not just at
;                its central velocity.
;   /nocolorbar Don't overplot the colorbar
;   position    The position to put the plot in, in normalized coordinates
;   /onlyim     Don't plot the colorbar and don't leave space for it.
;   /noerase    Don't erase the screen before you plot the image
;   charsize    Character size
;   colcharsize Character size for the colorbar alone
;   /avg        Color indicates the average of the third dimension
;   /maximum    Plot the maximum in the third dimension
;   /sqroot     Use the square-root for scaling
;   /column     Plot the N(HI) column density. N(HI) = 1.83E18 * Sum(T(B))*dv
;                  in units of 10^19 atoms/cm^2
;   minhue      The minimum hue value (between 0 and 360). For /AVG
;   maxhue      The maximum hue value (between 0 and 360). For /AVG
;   minbright   The minimum brightness value (between 0 and 1). For /AVG
;   maxbright   The maximum brightness value (between 0 and 1). For /AVG
;   saturation  The staturation value (between 0 and 1). For /AVG
;   year        Equinox for RA and DEC (default year=2000)
;   /radeg      RA in degrees otherwise in hours.
;   posim       Position of image (in normalized coordinates)
;   poscol      Positin of color bar (in normalized coordinates)
;   thick       The thickness of lines
;   charthick   The thickness of the annotations
;   framecolor   The color of the box and annotations
;   background_color The color of the background
;   invert      Black on white instead of white on black.
;   /center     The coordinates plotted should be the center of bins (default).
;   =xsize      Sets the x image size for PS output.
;   =ysize      Sets the y image size for PS output.
;   =ztop       The top for the z-values when using /avg
;   =zbot       The bottom for the z-values when using /avg
;   /wbot       Set the bottom color to white (i.e. the background color
;               of the actual image)
;   =colthick   The thickness of the colorbar
;   =colformat  The colorbar annotation format.
;   /rescale    Using the old rescaling scheme in display/imgscl
;
;  OUTPUTS
;   im          The image that is plotted
;   =xout       The array of x-values
;   =yout       The array of y-values
;   =xarr       The x-values of the image
;   =yarr       The y-values of the image
;   =out_posim  The position used for the image
;   =out_poscol The position used for the colorbar
;
; USAGE:
;   IDL>ghess,str,'lon','lat',dx=1,dy=1,/tot
;
; PROGRAMS USED:
;  TAG_PARSE.PRO Parse expressions for tags
;  GAREA.PRO     Calculates the area of a Gaussian
;  GNPOS.PRO     Returns the unique number of positions
;  DISPLAY.PRO   Display a 2D array
;   IMGSCL.PRO   Scales a 2D array for display.pro
;  COLORBAR.PRO  Creates a colorbar
;
;  REPSTR.PRO   IDL Astro Library
;
; Created by David Nidever May 2005
;-

t0 = systime(1)

ngstr = n_elements(gstr)
nxname = n_elements(xname)
nyname = n_elements(yname)

; Not enough inputs
if (n_params() eq 0) or (ngstr eq 0) or (nxname eq 0) or (nyname eq 0) then begin
  print,'Syntax - ghess,gstr,xname,yname,zname,im,color=color,nx=nx,ny=ny,dx=dx,dy=dy,'
  print,'               xtit=xtit,ytit=ytit,tit=tit,log=log,interpolate=interpolate,'
  print,'               noplot=noplot,save=save,file=file,xrange=xrange,yrange=yrange,'
  print,'               stp=stp,cut=cut,top=top,total=total,bot=bot,norm=norm,'
  print,'               nocolorbar=nocolorbar,spread=spread,position=position,'
  print,'               onlyim=onlyim,noerase=noerase,charsize=charsize,'
  print,'               avg=avg,minhue=minhue,maxhue=maxhue,minbright=minbright,'
  print,'               maxbright=maxbright, saturation=saturation, xflip=xflip,'
  print,'               yflip=yflip,year=year,ctool=ctool,xout=xout,yout=yout,'
  print,'               posim=posim,poscol=poscol,thick=thick,charthick=charthick,'
  print,'               framecolor=framecolor,background_color=background_color,'
  print,'               twocut=twocut,threecut=threecut,colcharsize=colcharsize,'
  print,'               invert=invert,center=center,xarr=xarr,yarr=yarr,xlog=xlog,'
  print,'               ylog=ylog,maximum=maximum,sqroot=sqroot,column=column,'
  print,'               xsize=xsize,ysize=ysize,out_posim=out_posim,out_poscol=out_poscol,'
  print,'               ztop=ztop,zbot=zbot,wbot=wbot,colthick=colthick,colformat=form,'
  print,'               coldivisions=coldivisions,xtickformat=xtickformat,ytickformat=ytickformat,'
  print,'               xtickname=xtickname,xtickv=xtickv,ytickname=ytickname,'
  print,'               ytickv=ytickv,xticks=xticks,yticks=yticks,xminor=xminor,yminor=yminor,'
  print,'               rescale=rescale'
  return
endif

START:

; ZNAME not set
if keyword_set(avg) and not keyword_set(zname) then begin
  case xname of
    'mlon': begin
              case yname of
                'mlat': zname = 'cen'
                'cen':  zname = 'mlat'
                 else:  goto,RETNOZNAME
              endcase
            end
    'mlat': begin
              case yname of
                'mlon': zname = 'cen'
                'cen':  zname = 'mlon'
                 else:  goto,RETNOZNAME
              endcase
            end
    'cen': begin
              case yname of
                'mlon': zname = 'mlat'
                'mlat': zname = 'mlon'
                 else:  goto,RETNOZNAME
              endcase
             end
     else: begin
             RETNOZNAME:
             print,'ZNAME IS REQUIRED WITH /AVG'
             return
           end
  endcase
endif

; TWOCUT and/or THREECUT
if keyword_set(twocut) or keyword_set(threecut) and not keyword_set(xrange) then $
  ghess_range_set,gstr,xname,yname,cut,twocut=twocut,threecut=threecut,$
                  xrange=xrange,yrange=yrange

; keywords
if keyword_set(spread) then total=0
if not keyword_set(zname) then zname=''
if not keyword_set(cut) then cut=''

npts = n_elements(gstr)

;if ((where(strlowcase([xname,yname,zname,cut]) eq 'area'))(0) ne -1) OR $
if total(stregex([xname,yname,zname,cut],'area',/boolean,/fold_case)) gt 0 OR $
  (keyword_set(total) or keyword_set(column) or keyword_set(avg)) then area = garea((gstr.par)(*))

if ((where(strlowcase([xname,yname,zname]) eq 'ra'))(0) ne -1) $
  and ((where(strlowcase([xname,yname,zname]) eq 'dec'))(0) ne -1) then begin
    if n_elements(year) eq 0 then year=2000.
    glactc,ra,dec,year,gstr.glon,gstr.glat,2,deg=radeg
    ; This is a kludge to make the magstream data continuous
    bdra = where(ra gt 10.0*(15^keyword_set(radeg)),nbdra)
    if nbdra gt 0 then ra(bdra) = ra(bdra)-24.0*(15^keyword_set(radeg))
endif


; Making the cut
if keyword_set(cut) then begin
  ; Replace tag names with full names, i.e ht -> gstr.ht

  ; Getting the structure tag names
  tags = tag_names(gstr)
  gtags = where(tags ne 'PAR' and tags ne 'SIGPAR',ngtags)

  cut2 = cut

  ; Only replace the PAR names with repstr
  origname = ['ht','cen','sig']
  replname = ['par[0]','par[1]','par[2]']

  ; Loop through the names to replace
  nrepl = n_elements(replname)
  for i=0,nrepl-1 do begin
    cut2 = repstr(cut2,origname[i],'gstr.'+replname[i])
  end

  ; Replace the rest with TAG_PARSE.PRO
  cut2 = tag_parse(cut2,tags,strname='gstr')

  ; Execute the cut
  outcut = execute('gd=where('+cut2+',ngd)')

  if keyword_set(area) then area = area[gd]
  if keyword_set(ra) then ra = ra[gd]
  if keyword_set(dec) then dec = dec[gd]

  orig_gstr = gstr

endif


; Getting x and y names
tags = tag_names(gstr)
gtags = where(tags ne 'PAR' and tags ne 'SIGPAR',ngtags)
names = [tags[gtags],'HT','CEN','SIG','AREA','RA','DEC']
names = strlowcase(names)      ; make them lowercase
; Are the X/Ynames okay?
xind = where(names eq strlowcase(xname),nxind)
yind = where(names eq strlowcase(yname),nyind)
if nxind eq 0 or nyind eq 0 then begin
  print,'Wrong X or Y name. Options: ht, cen, sig, area, mlon, mlat, glon, glat, ra or dec'
  return
endif

; Replace tag names with full names, i.e ht -> gstr.ht
inpnames = [xname,yname,zname]
if keyword_set(cut) then tag='[gd]' else tag=''

; Only replace the PAR names with repstr
origname = ['ht','cen','sig']
replname = ['par[0]','par[1]','par[2]']
 
; Loop through the names to replace
nrepl = n_elements(replname)
for i=0,nrepl-1 do begin
  inpnames = repstr(inpnames,origname[i],'gstr'+tag+'.'+replname[i])
end

; Replace the rest with TAG_PARSE.PRO
;for i=0,2 do inpnames[i] = TAG_PARSE(inpnames[i],tags,strname='gstr'+tag)
inpnames = TAG_PARSE(inpnames,tags,strname='gstr'+tag)

; Execute and get the X/Y/Z arrays
xname2 = inpnames(0)
yname2 = inpnames(1)
zname2 = inpnames(2)
outx = execute('x='+xname2)
outy = execute('y='+yname2)
if inpnames[2] ne '' then outz = execute('z='+zname2)

; Logarithmic
if keyword_set(xlog) then x = alog10(x)
if keyword_set(ylog) then y = alog10(y)

;DX not set
if not keyword_set(dx) and not keyword_set(nx) then begin
  if (where(['mlon','mlat','glon','glat','ra','dec'] eq strlowcase(xname)))(0) ne -1 then dx=0.5
  if strlowcase(xname) eq 'cen' then dx=1
  if strlowcase(xname) eq 'sig' then dx=1
  if strlowcase(xname) eq 'ht' then dx=0.05
  if strlowcase(xname) eq 'area' then dx=1

  ;nx = 200.
endif

;DY not set
if not keyword_set(dy) and not keyword_set(ny) then begin
  if (where(['mlon','mlat','glon','glat','ra','dec'] eq strlowcase(yname)))(0) ne -1 then dy=0.5
  if strlowcase(yname) eq 'cen' then dy=1
  if strlowcase(yname) eq 'sig' then dy=1
  if strlowcase(yname) eq 'ht' then dy=0.05
  if strlowcase(yname) eq 'area' then dy=1

  ;ny = 200.
endif

ymin = min(y)
ymax = max(y)
xmin = min(x)
xmax = max(x)

if keyword_set(xrange) and keyword_set(xlog) then xrange=alog10(xrange)
if keyword_set(yrange) and keyword_set(ylog) then yrange=alog10(yrange)

if keyword_set(xrange) then begin
  if (xrange(0) lt xmin) or (xrange(1) gt xmax) then begin
    xmin = xrange(0) < xmin
    xmax = xrange(1) > xmax
  endif
endif
if keyword_set(yrange) then begin
  if (yrange(0) lt ymin) or (yrange(1) gt ymax) then begin
    ymin = yrange(0) < ymin
    ymax = yrange(1) > ymax
  endif
endif

if keyword_set(ny) and keyword_set(nx) then begin
  dy = (ymax-ymin)/(ny-1.)
  dx = (xmax-xmin)/(nx-1.)
endif else begin
  if not keyword_set(dx) then dx = 0.5
  if not keyword_set(dy) then dy = 0.5
  ny = ceil((ymax-ymin)/dy) + 1.
  nx = ceil((xmax-xmin)/dx) + 1.
endelse

im = fltarr(nx,ny)
imind = strarr(nx,ny)
ng = n_elements(x)

; CREATING THE IMAGE

yarr = findgen(ny)*dy+ymin
xarr = findgen(nx)*dx+xmin

; Center the coordinates
if n_elements(center) eq 0 then center=1
if keyword_set(center) then begin
 xarr = xarr+0.5*dx
 yarr = yarr+0.5*dy
end


;#####################
; Number of gaussians
;#####################
if not keyword_set(total) and not keyword_set(spread) and not keyword_set(avg) then $
  ++im( floor((x-xmin)/dx), floor((y-ymin)/dy) )
; OLD WAY
;for i=0.,ng-1. do dum = ++im( floor((x(i)-xmin)/dx), floor((y(i)-ymin)/dy) )

;############
; Total area
;############
if keyword_set(total) then begin
   
  ; Histogram
  numim = im*0.
  ++numim( floor((x-xmin)/dx), floor((y-ymin)/dy) )


  ; LOTS OF POINTS
  ; Must not have too many in each pixel otherwise it requires
  ;  too many loops.
  IF (n_elements(x) gt 1e5) and (max(numim) lt 1000.) then begin

    ; THE METHOD USED HERE:
    ; When you doing an assignment operation while subscripting
    ; an array with vectors and subscripts are REPEATED then
    ; the value of the LAST subscript gets used/assigned.
    ;
    ; So in order to get the area of each point in a pixel
    ; I loop through the "layers" of points.  Each time a layer
    ; has been added those indices have to be removed.


    ; Which pixels have points?
    havepts = where(numim gt 0,nhavepts)

    ; Initalize arrays
    indall = im*0.
    area2 = area
    xind2 = floor((x-xmin)/dx)
    yind2 = floor((y-ymin)/dy)
    if keyword_set(norm) then begin
      ;imind = strarr(nx,ny)  ; defined above
      tempind = strarr(nx,ny)
      origind = strtrim(L64indgen(n_elements(area)),2)+' '
    endif

    ; Loop through "layers" until done
    flag = 0
    count = 0
    while (flag ne 1) do begin

      ; How many points to we have now
      narea2 = n_elements(area2)
      ; 1D array of indices for the arrays
      ;   for this "layer"
      ind2 = findgen(narea2)

      ; Area for this "layer"
      temp = im*0.
      temp[xind2,yind2] = area2

      ; Indices for this "layer"
      ;  The last subscript gets assigned
      indall = im*0.-1
      indall[xind2,yind2] = ind2

      ; Original indices
      if keyword_set(norm) then begin
        tempind[*,*] = ''
        tempind[xind2,yind2] = origind
      endif

      ; Get the indices used
      ;  Only want the pixels that have points
      gg = where( (indall)(havepts) gt -1,ngg)
      ;gg = where( indall gt -1,ngg)

      ; We're done.  No points left
      if (ngg eq 0) or (ngg eq narea2) then begin

        flag = 1

      ; Remove the indices used
      endif else begin

        ; These are the indices used
        badind = (indall)(havepts[gg])
        ;badind = indall[gg]
        ; Remove the indices used from all 1D arrays
        if keyword_set(norm) then begin
          remove,badind,ind2,xind2,yind2,area2,origind
        endif else begin
          remove,badind,ind2,xind2,yind2,area2
        endelse

        ; Increment the counter
        ++count

      endelse

      ; Add this layer to the final image
      im = im + temp
      if keyword_set(norm) then $
        imind = imind +' '+ tempind

    end ; while loop

    if keyword_set(norm) then $
      imind = strtrim(imind,2)

  ; Few points
  ENDIF ELSE BEGIN

    ; OLD METHOD
    for i=0.,ng-1. do begin
      xind = floor((x(i)-xmin)/dx)
      yind = floor((y(i)-ymin)/dy)
      im(xind,yind) = im(xind,yind)+area(i)
      ;im(xind,yind) = im(xind,yind)+garea([ht(i),0.,sig(i)])
      imind(xind,yind) = imind(xind,yind)+strtrim(i,2)+' '
    endfor

  ENDELSE ; few points

endif


;################
; Column Density
;################
if keyword_set(column) then begin
  for i=0.,ng-1. do begin
    xind = floor((x(i)-xmin)/dx)
    yind = floor((y(i)-ymin)/dy)
    im(xind,yind) = im(xind,yind)+area(i)
    ;im(xind,yind) = im(xind,yind)+garea([ht(i),0.,sig(i)])
    imind(xind,yind) = imind(xind,yind)+strtrim(i,2)+' '
  endfor
  im = im*1.83d18/1d19  ; in units of 10^19 atoms/cm^2
endif


;################################
; Spreading out the intensity
;################################
if keyword_set(spread) then begin
  if xname eq 'cen' or yname eq 'cen' then begin

    if keyword_set(cut) then tag='(gd)' else tag=''
    htname = 'gstr'+tag+'.par(0)'
    cenname = 'gstr'+tag+'.par(1)'
    signame = 'gstr'+tag+'.par(2)'
    dum = execute('ht = '+htname)
    dum = execute('cen = '+cenname)
    dum = execute('sig = '+signame)

    if (xname eq 'cen') then begin
      ; looping through all the gaussians
      for i=0.,ng-1 do begin
        im(*,floor((y(i)-ymin)/dy)) = im(*,floor((y(i)-ymin)/dy)) + gfunc(xarr,[ht(i),cen(i),sig(i)])
      end
    endif

    if (yname eq 'cen') then begin
      ; looping through all the gaussians
      for i=0.,ng-1 do begin
        im(floor((x(i)-xmin)/dx),*) = im(floor((x(i)-xmin)/dx),*) + gfunc(yarr,[ht(i),cen(i),sig(i)])
      end
    endif

  endif else begin
    print,'TO USE /SPREAD ONE OF THE VARIABLES MUST BE _CEN_'
    return
  endelse

endif


;############
; AVERAGE
;############
if keyword_set(avg) then begin

  if not keyword_set(zname) then begin
    print,'ZNAME IS REQUIRED WITH /AVG'
    return
  endif
  outz = execute('z='+zname2)

  ; LOTS OF POINTS
  IF (n_elements(x) gt 1e5) then begin

    ; Three 2D arrays
    ;  im     Total
    ;  ima    Weighted average (i.e. sum of area*z)
    ;  imn    # of Gaussians
    ;  imind  Array of original indices of the
    ;          Gaussians in that pixel.  Used to normalize
    ima = im*0.
    imn = im*0.
    ;if keyword_set(norm) then $     ; defined above
    ;  imind = strarr(nx,ny)


    ; Histogram
    ++imn( floor((x-xmin)/dx), floor((y-ymin)/dy) )

    ; Which pixels have points?
    havepts = where(imn gt 0,nhavepts)

    ; Initalize arrays

    indall = im*0.
    area2 = area
    warea2 = area * z
    xind2 = floor((x-xmin)/dx)
    yind2 = floor((y-ymin)/dy)
    if keyword_set(norm) then begin
      tempind = strarr(nx,ny)
      origind = strtrim(L64indgen(n_elements(area)),2)+' '
    endif

    ; Loop through "layers" until done
    flag = 0
    count = 0
    while (flag ne 1) do begin

      ; How many points to we have now
      narea2 = n_elements(area2)
      ; 1D array of indices for the arrays
      ;   for this "layer"
      ind2 = findgen(narea2)

      ; Area for this "layer"
      temp = im*0.
      tempa = im*0.
      temp[xind2,yind2] = area2
      tempa[xind2,yind2] = warea2

      ; Indices for this "layer"
      ;  The last subscript gets assigned
      indall = im*0.-1
      indall[xind2,yind2] = ind2

      ; Original indices
      if keyword_set(norm) then begin
        tempind[*,*] = ''
        tempind[xind2,yind2] = origind
      endif

      ; Get the indices used
      ;  Only want the pixels that have points
      gg = where( (indall)(havepts) gt -1,ngg)

      ; We're done.  No points left
      if (ngg eq 0) or (ngg eq narea2) then begin

        flag = 1

      ; Remove the indices used
      endif else begin

        ; These are the indices used
        badind = (indall)(havepts[gg])
        ; Remove the indices used from all 1D arrays
        if keyword_set(norm) then begin
          remove,badind,ind2,xind2,yind2,area2,warea2,origind
        endif else begin
          remove,badind,ind2,xind2,yind2,area2,warea2
        endelse

        ; Increment the counter
        ++count

      endelse

      ; Add this layer to the final image
      im = im + temp
      ima = ima + tempa
      if keyword_set(norm) then $
        imind = imind +' '+ tempind

      ;stop

    end ; while loop

    if keyword_set(norm) then $
      imind = strtrim(imind,2)

  ; FEW POINTS
  ENDIF ELSE BEGIN

    ; OLD METHOD
    ; Total and Average
    ima = im      ; average
    imn = im      ; number of gaussians
    im = im*0.0   ; start fresh
    for i=0.,ng-1. do begin
      xind = floor((x(i)-xmin)/dx)
      yind = floor((y(i)-ymin)/dy)
      im(xind,yind) = im(xind,yind)+area(i)
      ima(xind,yind) = ima(xind,yind)+area(i)*z(i)
      ;im(xind,yind) = im(xind,yind)+garea([ht(i),0.,sig(i)])
      ;ima(xind,yind) = ima(xind,yind)+garea([ht(i),0.,sig(i)])*z(i)
      imind(xind,yind) = imind(xind,yind)+strtrim(i,2)+' '
      dum = ++imn( floor((x(i)-xmin)/dx), floor((y(i)-ymin)/dy) )
    endfor

  ENDELSE ; few points

  dum = im
  bd = where(dum eq 0.,nbd)
  if nbd gt 0 then (dum)(bd) = 1.
  ima = ima/dum   ; dividing by total area

  ; Dividing by # of positions in bin
  if keyword_set(norm) then begin

    ; Looping through the image elements
    ind = where(im gt 0.,nind)
    for i=0.,nind-1 do begin
      ind2 = array_indices(im,ind(i))
      ig = float( strsplit(imind(ind2(0),ind2(1)),' ',/extract) )
      nig = n_elements(ig)
      ;ig = where(floor((x-xmin)/dx) eq ind2(0) and floor((y-ymin)/dy) eq ind2(1), nig)
      if nig gt 0 then begin
        npos = gnpos(gstr(ig))
        im(ind2(0),ind2(1)) = im(ind2(0),ind2(1))/float(npos)
      endif ; nind > 0
    end ; for i

  endif  ; norm

  if keyword_set(sqroot) then im = sqrt(im)

  ; TOP, integrated intensity
  if keyword_set(top) then begin
    tbd = where(im gt top,ntbd)
    if ntbd gt 0 then (im)(tbd) = top
  endif

  ; BOT, integrated intensity
  if keyword_set(bot) then begin
    bbd = where(im lt bot,nbbd)
    if nbbd gt 0 then (im)(bbd) = bot
  endif

  byte_im = ImgScl(im, Min=bot, Max=top, $
		   Log=log, Levels=l, MaskValue=maskvalue)
  im = byte_im

  ; White for bottom color
  if keyword_set(wbot) then begin
    wmask = float(im eq 1.0)
    ;wbd = where(im eq 1.0,nwbd)
    ;ind2d = array_indices(im,wbd)
  end

  if n_elements(ztop) eq 0 then ztop=max(ima)
  if n_elements(zbot) eq 0 then zbot=min(ima)

  ; Keeping the Average within the Z range
  low = where(ima lt min(z),nlow)
  if nlow gt 0 then ima[low] = min(z)
  hi = where(ima gt max(z),nhi)
  if nhi gt 0 then ima[hi] = max(z)

  ; ZTOP, z-values
  if keyword_set(ztop) then begin
    ztbd = where(ima gt ztop,nztbd)
    if nztbd gt 0 then (ima)(ztbd) = ztop
  endif

  ; ZBOT, z-values
  if keyword_set(zbot) then begin
    zbbd = where(ima lt zbot,nzbbd)
    if nzbbd gt 0 then (ima)(zbbd) = zbot
  endif

  ; convert image to RGB, using HLS
  ; hue is Average (IMA)   (0-360)
  ; 0-red, 120-green, 240-blue
  ; brightness is Total (im) (0-1)
  ima2 = -ima    ; (blue-green-red)
  if not keyword_set(minhue) then minhue = 0.
  if not keyword_set(maxhue) then maxhue = 240.
  if not keyword_set(minbright) then minbright = 0.10
  if not keyword_set(maxbright) then maxbright = 0.70
  if not keyword_set(saturation) then saturation = 0.9
  
  hue = scale(ima2,[-ztop,-zbot],[minhue,maxhue])
  ;hue = scale_vector(ima2,minhue,maxhue)
  bright = scale_vector(im,minbright,maxbright)

  color_convert, hue, bright, im*0.+saturation, r, g, b, /HLS_RGB
  ;color_convert, hue, im*0.+1.0, bright, r, g, b, /HSV_RGB

  ; setting bottom to zero
  if keyword_set(bot) and keyword_set(bbd) then begin
    (r)(bbd) = 0.
    (g)(bbd) = 0.
    (b)(bbd) = 0.
  endif

  ;bd = where(ima eq 0. or im eq 0.,nbd)
  ;if nbd gt 0 then begin
  ;  (r)(bd) = 255
  ;  (g)(bd) = 255
  ;  (b)(bd) = 255
  ;endif

  ; Interleaved image
  im2 = bytarr(3,nx,ny)
  im2(0,*,*) = r
  im2(1,*,*) = g
  im2(2,*,*) = b

  ; Final image to plot
  orig_im = im
  im = im2

  ; White for bottom color
  if keyword_set(wbot) then begin
    if wbot[0] ne 1 then wbotcol = wbot else wbotcol=[255,255,255]
    if n_elements(wbotcol) eq 1 then wbotcol=[1,1,1]*wbotcol
    im[0,*,*] = reform(im[0,*,*])*(1.0-wmask) + wmask*wbotcol[0]
    im[1,*,*] = reform(im[1,*,*])*(1.0-wmask) + wmask*wbotcol[1]
    im[2,*,*] = reform(im[2,*,*])*(1.0-wmask) + wmask*wbotcol[2]
  end

  if n_elements(tit) eq 0 then tit = 'COLOR AS '+strupcase(zname)

endif ; avg


;##########
; MAXIMUM
;##########
if keyword_set(maximum) then begin

  if not keyword_set(zname) then begin
    print,'ZNAME IS REQUIRED WITH /AVG'
    return
  endif
  outz = execute('z='+zname2)

  for i=0.,ng-1. do begin
    xind = floor((x(i)-xmin)/dx)
    yind = floor((y(i)-ymin)/dy)
    im(xind,yind) = im(xind,yind) > z(i)
  end

end


;####################################
; Dividing by # of positions in bin
;####################################
if keyword_set(norm) and not keyword_set(avg) then begin

  ; Looping through the image elements
  ind = where(im gt 0.,nind)
  for i=0.,nind-1 do begin
    ind2 = array_indices(im,ind(i))
    ig = float( strsplit(imind(ind2(0),ind2(1)),' ',/extract) )
    nig = n_elements(ig)
    ;ig = where(floor((x-xmin)/dx) eq ind2(0) and floor((y-ymin)/dy) eq ind2(1), nig)
    if nig gt 0 then begin
      npos = gnpos(gstr(ig))
      im(ind2(0),ind2(1)) = im(ind2(0),ind2(1))/float(npos)
    endif ; nind > 0
  end ; for i

endif  ; norm


;####################################
; TOP and BOT (not /avg, has its own)
;####################################
if not keyword_set(avg) then begin

  ; top
  if n_elements(top) gt 0. then begin
    bd=where(im ge top,nbd)
    if nbd gt 0 then im(bd) = top
  endif

  ; bot
  if n_elements(bot) gt 0. then begin
    bd=where(im le bot,nbd)
    if nbd gt 0 then im(bd) = bot
  endif
endif


;#########################
; TWOCUT or/and THREECUT
;#########################
if keyword_set(twocut) or keyword_set(threecut) then begin
  
  szim = size(im)
  im1 = im
  im = fltarr(3,szim(1),szim(2))
  im(0,*,*) = im1

  if keyword_set(twocut) then begin
    ghess,orig_gstr,xname,yname,zname,imtwo,color=color,nx=nx,ny=ny,dx=dx,dy=dy,$
          log=log,interpolate=interpolate,xrange=xrange,yrange=yrange,$
          cut=twocut,top=top,bot=bot,norm=norm,avg=0,total=total,$
          spread=spread,xflip=xflip,yflip=yflip,year=year,/noplot

    im(1,*,*) = imtwo
  endif

  if keyword_set(threecut) then begin
    ghess,orig_gstr,xname,yname,zname,imthree,color=color,nx=nx,ny=ny,dx=dx,dy=dy,$
          log=log,interpolate=interpolate,xrange=xrange,yrange=yrange,$
          cut=threecut,top=top,bot=bot,norm=norm,avg=0,total=total,$
          spread=spread,xflip=xflip,yflip=yflip,year=year,/noplot

    im(2,*,*) = imthree

  endif

endif


;######################################
; SQUARE-ROOT, /avg does it separately
;######################################
if keyword_set(sqroot) and not keyword_set(avg) then im=sqrt(im)

; Using only a certain range
if keyword_set(xrange) then begin
  dum = closest(xrange(0),xarr,ind=xlo)
  dum = closest(xrange(1),xarr,ind=xhi)
  imsz = size(im)
  if imsz(0) eq 3 then im = im(*,xlo:xhi,*) else im=im(xlo:xhi,*)
  xarr = xarr(xlo:xhi)
endif
if keyword_set(yrange) then begin
  dum = closest(yrange(0),yarr,ind=ylo)
  dum = closest(yrange(1),yarr,ind=yhi)
  imsz = size(im)
  if imsz(0) eq 3 then im = im(*,*,ylo:yhi) else im=im(*,ylo:yhi)
  yarr = yarr(ylo:yhi)
endif


;############
; Plotting
;############
if not keyword_set(noplot) then begin
  if not keyword_set(file) then file='ghess'

  if not keyword_set(thick) then thick=1.0

  if keyword_set(save) then begin
    if not keyword_set(thick) then psthick=3 else psthick=0   ; make thick lines by default
    ps_open,file,color=color,thick=psthick
    ;if keyword_set(color) then loadct,39
    ;notop=1

    ; Assigning bottom values to the top
    ; most color (white)
    ;bd = where(im eq min(im),nbd)
    ;gd = where(im ne min(im),ngd)
    ;tmin = min(im(gd))
    ;tmax = max(im(gd))
    ;ncolor = 256.
    ;dim = (tmax-tmin)/ncolor
    ;im(bd) = tmax+dim

  endif else begin
    if (!d.name ne 'PS' and !d.name ne 'Z') then begin
      if keyword_set(color) then begin
        ;loadct,39
        ;device,decomposed=0
      endif ;else device,decomposed=1
    endif else begin
      ;loadct,39
    endelse
  endelse

  ;; Using only a certain range
  ;if keyword_set(xrange) then begin
  ;  dum = closest(xrange(0),xarr,ind=xlo)
  ;  dum = closest(xrange(1),xarr,ind=xhi)
  ;  imsz = size(im)
  ;  if imsz(0) eq 3 then im = im(*,xlo:xhi,*) else im=im(xlo:xhi,*)
  ;  xarr = xarr(xlo:xhi)
  ;endif
  ;if keyword_set(yrange) then begin
  ;  dum = closest(yrange(0),yarr,ind=ylo)
  ;  dum = closest(yrange(1),yarr,ind=yhi)
  ;  imsz = size(im)
  ;  if imsz(0) eq 3 then im = im(*,*,ylo:yhi) else im=im(*,ylo:yhi)
  ;  yarr = yarr(ylo:yhi)
  ;endif

  ;if keyword_set(xreverse) then begin
  ;  im = reverse(im)
  ;  xarr = xarr(im)
  ;endif


  ;axis titles
  ndec = 1
  if keyword_set(ra) or keyword_set(dec) then if long(year)-float(year) eq 0.0 then ndec=0
  if keyword_set(year) then stryear = stringize(year,/nocomma,ndec=ndec)
  if not keyword_set(xtit) then xtit=strupcase(xname)
  if strlowcase(xname) eq 'ra' or strlowcase(xname) eq 'dec' then xtit=strupcase(xname)+' (J'+stryear+')'
  if not keyword_set(ytit) then ytit=strupcase(yname)
  if strlowcase(yname) eq 'ra' or strlowcase(yname) eq 'dec' then ytit=strupcase(yname)+' (J'+stryear+')'
  if n_elements(tit) eq 0 then begin
    tit=strlowcase(yname)+' vs. '+strlowcase(xname)
    if keyword_set(total) or keyword_set(spread) then tit='Total AREA ('+tit+')'
    if not keyword_set(total) and not keyword_set(spread) then tit='Number of Gaussians ('+tit+')'
    if keyword_set(maximum) then tit='MAXIMUM '+zname
    if keyword_set(column) then tit='Column Density (10!u19!n atoms/cm!u2!n)'
  endif

  ; Plotting it
  ;if not keyword_set(position) then position = [0.,0.,1.,1.]
  ;dx1 = position(2)-position(0)
  ;dy1 = position(3)-position(1)
  ;x0 = position(0)
  ;y0 = position(1)
  ;if not keyword_set(onlyim) then $
  ;pos = [0.08*dx1+x0,0.10*dy1+y0,0.95*dx1+x0,0.85*dy1+y0]
  ;if keyword_set(onlyim) then $
  ;pos = [0.08*dx1+x0,0.10*dy1+y0,0.95*dx1+x0,0.95*dy1+y0]

  if keyword_set(posim) then pos = posim

  ;pos = [0.094*dx1+x0,0.078*dy1+y0,0.97*dx1+x0,0.96*dy1+y0]
  ;position = [ 0.0937550, 0.078130, 0.973443, 0.962896]
  ;pos = [0.08,0.10,0.95,0.85]

  oldp = !p
  if not keyword_set(onlyim) then !p.region = [0.,0.,1.0,0.9]
  if keyword_set(position) then begin
    dy = position(3)-position(1)
    !p.region=[position(0),position(1),position(2),position(1)+0.9*dy]
    if keyword_set(onlyim) then !p.region = position
  endif

  pim = im
  if keyword_set(invert) then pim=-pim

  ; Putting the x and y-arrays back on the linear scale
  ;  so the axis scale will show the linear values, but on a log scale
  if keyword_set(xlog) then xarr = 10.^xarr
  if keyword_set(ylog) then yarr = 10.^yarr

  display,pim,xarr,yarr,interpolate=interpolate,log=log,xtit=xtit,$
          ytit=ytit,tit=tit,pos=pos,notop=notop,noerase=noerase,$
          charsize=charsize,xflip=xflip,yflip=yflip,thick=thick,$
          charthick=charthick,framecolor=framecolor,$
          background_color=background_color,color=color,xlog=xlog,$
          ylog=ylog,xsize=xsize,ysize=ysize,xtickformat=xtickformat,$
          ytickformat=ytickformat,xtickname=xtickname,xtickv=xtickv,$
          ytickname=ytickname,ytickv=ytickv,xticks=xticks,yticks=yticks,$
          xminor=xminor,yminor=yminor,min=bot,max=top,rescale=rescale

  ;!p.region = [0.,0.9,1.0,1.0]
  ;!p = oldp
  !p.region = oldp.region
  ; This is the position of the display box output from display.pro
  ; but relative to !p.region
  if n_elements(position) eq 0 then begin
    y2 = 1.0
    dy1 = 1.0
  endif else begin
    y2 = position(3)
    dy1 = position(3)-position(1)
  endelse
  position2 = pos
  dx2 = position2(2)-position2(0)
  dy2 = position2(3)-position2(1)
  x0 = position2(0)
  y0 = position2(1)
  ;colpos = [x0,0.94,x0+dx2,0.97]
  colpos = [x0,y2-0.06*dy1,x0+dx2,y2-0.03*dy1]

  ;colpos = [0.08*dx2+x0,0.92*dy2+y0,0.95*dx2+x0,0.95*dy2+y0]
  ;colpos = [0.08,0.92,0.95,0.95]
  if keyword_set(poscol) then colpos = poscol

  ; Outputting the positions
  out_poscol = colpos
  out_posim = pos


  ; Overplotting the colorbar
  if not keyword_set(nocolorbar) and not keyword_set(onlyim) then begin
    ;if keyword_set(color) then loadct,39,/silent

    if not keyword_set(charsize) then charsize=1.0
    minim = min(im)
    maxim = max(im)
    if keyword_set(avg) then begin
      ;minim = min(z)
      ;maxim = max(z)
      minim = min(ima)
      maxim = max(ima)
      if keyword_set(ztop) then maxim = ztop
      if keyword_set(zbot) then minim = zbot
    endif

    len = strlen(strtrim(long(maxim),2))
    if minim lt 0. then len = len+1
    if not keyword_set(form) then begin
      if maxim lt 100 then form = '(F'+strtrim(len+3,2)+'.1)'
      if maxim ge 100 then form = '(I'+strtrim(len,2)+')'
    endif
    ;if not keyword_set(color) then loadct,0,/silent
    if keyword_set(log) and not keyword_set(avg) then begin
      xlog = 1
      minor = 9
      divisions = 0
    endif
    if keyword_set(coldivisions) then divisions=coldivisions
    ;if minim eq 0. then minrange = 1. else minrange = minim
    minrange = minim
    if minim eq 0. and keyword_set(log) then minrange = 1.
    maxrange= maxim

    if not keyword_set(colthick) then colthick=thick


    if not keyword_set(twocut) and not keyword_set(threecut) then begin

      ; Scale of colors
      if keyword_set(avg) then begin
        bottom=50
        ncolors=200
      endif else begin
        bottom=1 ;0       ;10
        ncolors=254 ;255    ;245
      endelse

      if not keyword_set(colcharsize) then colcharsize=charsize

      df_colorbar,position=colpos,minrange=minrange,maxrange=maxrange,$
                charsize=colcharsize,format=form,bottom=bottom,ncolors=ncolors,$
                xlog=xlog,minor=minor,divisions=divisions,thick=colthick,$
                charthick=charthick,color=framecolor,xthick=colthick,$
                ythick=colthick,invertcolor=invert
    endif else begin

      bar = bytarr(3,256,30)
      ncut = 0
      if keyword_set(cut) then ncut = ncut + 1
      if keyword_set(twocut) then ncut = ncut + 1
      if keyword_set(threecut) then ncut = ncut + 1

      if keyword_set(cut) then begin
        if ncut eq 2 then bar(0,*,0:14) = bindgen(256) # replicate(1B, 15)
        if ncut eq 3 then bar(0,*,0:9) = bindgen(256) # replicate(1B, 10)
      endif
      if keyword_set(twocut) then begin
        if ncut eq 2 and keyword_set(cut) then $
          bar(1,*,15:29) = bindgen(256) # replicate(1B, 15)
        if ncut eq 2 and keyword_set(threecut) then $
          bar(1,*,0:14) = bindgen(256) # replicate(1B, 15)
        if ncut eq 3 then bar(1,*,10:19) = bindgen(256) # replicate(1B, 10)
      endif
      if keyword_set(threecut) then begin
        if ncut eq 2 and keyword_set(cut) then $
          bar(2,*,15:29) = bindgen(256) # replicate(1B, 15)
        if ncut eq 2 and keyword_set(twocut) then $
          bar(2,*,0:14) = bindgen(256) # replicate(1B, 15)
        if ncut eq 3 then bar(2,*,20:29) = bindgen(256) # replicate(1B, 10)
      endif

      ;loadct,0,/silent
      if not keyword_set(colcharsize) then colcharsize=charsize
      colorbar,position=colpos,minrange=minrange,maxrange=maxrange,$
                charsize=colcharsize,format=form,bottom=0,ncolors=256.,$
                xlog=xlog,minor=minor,divisions=divisions,thick=thick,$
                charthick=charthick,color=framecolor,xthick=thick,$
                ythick=thick,bar=bar

    endelse

  endif ; not /nocolorbar

  if keyword_set(save) then ps_close

endif ; not /noplot

;; Using GHESS_CUT.PRO
;if keyword_set(ctool) and not keyword_set(fcut) then begin
;  ghess_cut,xr=xrange,yr=yrange,xflip=xflip,yflip=yflip,fcut=fcut,xname=xname,yname=yname,$
;            loarr=loarr,hiarr=hiarr
;  cut = '(' + cut + ') AND (' + fcut +')'
;  goto,START
;end

xout = x
yout = y

;!p.region=0

if keyword_set(stp) then stop

if keyword_set(orig_gstr) then gstr = orig_gstr

end
