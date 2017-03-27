TexConv2.exe -i .dds -o 2.gtx
TexConv2.exe -i 2.gtx -f GX2_SURFACE_FORMAT_ -tileMode GX2_TILE_MODE_ -o .gtx
DEL 2.gtx
PAUSE