read -p "Enter text or call: " ANSWER
echo $ANSWER
read -p "Enter number: " NUMBER
echo $NUMBER
read -p "Enter message: " MESSAGE
MESSAGE=${MESSAGE// /%20}
echo $MESSAGE
curl http://45.56.125.90:5000/$ANSWER/$NUMBER/$MESSAGE

