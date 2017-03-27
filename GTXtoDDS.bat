MKDIR DDS\
for %%f in (*.gtx) do TexConv2.exe -i %%f -f GX2_SURFACE_FORMAT_TCS_R8_G8_B8_A8_UNORM -o DDS\%%f
for %%f in (DDS\*.gtx) do gtx_extract.exe %%f
DEL DDS\*.gtx