P1="${HOME}/.m2/repository/com/google/code/gson/gson/2.8.2/gson-2.8.2.jar"
P2="target/tester-1.0-SNAPSHOT.jar"
CP="$P1:$P2"
echo $CP
java -cp $CP com.alarm2.App


