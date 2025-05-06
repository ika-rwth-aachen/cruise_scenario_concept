for /R %%f in (*.dot) do (
    echo %%f
    dot -T svg -O "%%f"
)
