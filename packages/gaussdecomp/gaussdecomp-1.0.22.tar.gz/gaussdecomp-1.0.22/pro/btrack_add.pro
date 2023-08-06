pro btrack_add,track
;;  This adds new elements to btrack

ntrack = n_elements(track)

np = 99
btrack_schema = {count:999999.,lon:999999.,lat:999999.,rms:999999.,noise:999999.,par:fltarr(np)+999999,$
                 guesspar:fltarr(np)+999999.,guesslon:999999.,guesslat:999999.,back:999999.,redo:999999.,$
                 redo_fail:999999.,skip:999999.,lastlon:999999.,lastlat:999999.}

DEFSYSV,'!btrack',exists=btrack_exists
if not keyword_set(btrack_exists) then begin
  DEFSYSV,'!btrack',{data:ptr_new(),ndata:0LL,count:0LL}
  !btrack.data = ptr_new(replicate(btrack_schema,100000L))
  !btrack.ndata = 100000LL
  !btrack.count = 0LL
endif

;; Add more gaussian parameter elements, PAR
if n_elements(track[0].par) gt n_elements((*(!btrack.data))[0].par) then begin
  print,'Increasing the number elements of PAR in BTRACK'
  data = *(!btrack.data)
  ndata = !btrack.ndata
  count = !btrack.count
  gbtrack,data,track  ;; this fixes the structure
  ;; New structure
  np = n_elements(track[0].par)
  btrack_schema = {count:999999.,lon:999999.,lat:999999.,rms:999999.,noise:999999.,par:fltarr(np)+999999,$
                   guesspar:fltarr(np)+999999.,guesslon:999999.,guesslat:999999.,back:999999.,redo:999999.,$
                   redo_fail:999999.,skip:999999.,lastlon:999999.,lastlat:999999.}  
  !btrack.data = ptr_new(data)
  !btrack.ndata = ndata
  !btrack.count = count
endif

;; Add new elements
if ntrack+!btrack.count gt !btrack.ndata then begin
  print,'Adding more rows to BTRACK'
  data = *(!btrack.data)
  ndata = !btrack.ndata
  cont = !btrack.count
  newdata = replicate(btrack_schema,ndata+100000L)
  newdata[0:ndata-1] = data
  nnewdata = long64(n_elements(newdata))
  !btrack.data = ptr_new(newdata)
  !btrack.nnewdata
  !btrack.count = count
endif
;; Stuff in the new data
temp = *(!btrack.data)
temp[!btrack.count:!btrack.count+ntrack-1] = track
!btrack.data = ptr_new(temp)
undefine,temp
!btrack.count += ntrack

end
