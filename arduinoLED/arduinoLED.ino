int greenPin = 10;
int bluePin = 11;
int redPin = 12;

int rVal = 254;
int gVal = 1;
int bVal = 127;

int rDir = -1;
int gDir = 1;
int bDir = -1;

int inByte = 0;

boolean christmastState = false;

void setup() {
  Serial.begin(9600);
  pinMode(greenPin, OUTPUT);
  pinMode(bluePin, OUTPUT);
  pinMode(redPin, OUTPUT);
  Serial.println("you can start sending information!");
}

void loop() {
  if (christmastState) {
    chirstmasLoop();
  }
  if (Serial.available() > 0) {
    inByte = Serial.read(); // yes, so read it from incoming buffer
    if (inByte == 'a')
    {
      christmastState = true;
      //digitalWrite(greenPin, LOW);
    }
    else if (inByte == 'b')
    {
      christmastState = false;
      allOff();
      //digitalWrite(bluePin, LOW);
    }
    else if (inByte == 'c')
    {
      digitalWrite(redPin, LOW);
    }
    else if (inByte == 'd')
    {
      digitalWrite(greenPin, HIGH);
      digitalWrite(bluePin, HIGH);
      digitalWrite(redPin, HIGH);
    }
  }
}

int chirstmasLoop() {

  analogWrite(redPin, rVal);
  analogWrite(greenPin, gVal);
  analogWrite(bluePin, bVal);

  rVal = rVal + rDir;
  gVal = gVal + gDir;
  bVal = bVal + bDir;

  if (rVal >= 255 || rVal <= 0) {
    rDir = rDir * -1;
  }

  if (gVal >= 255 || gVal <= 0) {
    gDir = gDir * -1;
  }

  if (bVal >= 255 || bVal <= 0) {
    bDir = bDir * -1;
  }

  // slight delay so it doesn't rotate color too quicky
  delay(1);

}
void allOff() {
  digitalWrite(greenPin, HIGH);
  digitalWrite(bluePin, HIGH);
  digitalWrite(redPin, HIGH);
}
