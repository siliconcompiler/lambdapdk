# Step 1: merge in latest updates from main/master
git submodule update --init --remote --merge

# Step 2: add any changed submodules
git add submodules/

# Step 3: commit changes
git commit -m "Update submodules" -e

echo ""
echo "NOTE:"
echo "Be sure to push any changed submodules before pushing ebrick!"
echo "Run $ git submodule foreach --recursive \"git push\" to do this automatically."

