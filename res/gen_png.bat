for /R %%f in (*.dot) do (
    echo %%f
    dot -T png -O "%%f"
)
