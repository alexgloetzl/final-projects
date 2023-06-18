// Final project of the microcontroller lecture WS 22/23
// Infrared controlled car

// written by Alex Glötzl
// with the help of my supervisor Lukas Böhm, who contributed the NEC protocol


#ifndef __AVR_ATmega328P__
    #define __AVR_ATmega328P__
#endif

#define F_CPU 16000000UL

#include <avr/io.h>
#include <avr/interrupt.h>
#include <stdlib.h>
#include <stdio.h>

#define IR_BUTTON_forward 0xF8C7
#define IR_BUTTON_backward 0xFA55
#define IR_BUTTON_forward_right 0xFBD4
#define IR_BUTTON_forward_left 0xF986
#define IR_BUTTON_backward_right 0xFA95
#define IR_BUTTON_backward_left 0xFA15


#define setbit(port,bit)  ((port) |=  (1<<bit)) 
#define clrbit(port,bit)  ((port) &= ~(1<<bit)) 

#define ICP_PIN PB0   // use ICP1 pin as input

uint16_t pulszeit;
uint8_t bitZahl=0;
uint8_t startBit=0;
volatile unsigned int IR_Code=0;
uint8_t knopf_druck;

volatile uint16_t pulsweite;
volatile uint16_t pulsweite_array[32+1];
volatile uint8_t daten_verarbeiten=0;

volatile uint8_t i;
volatile uint32_t counter;


int uart_putc(unsigned char c)
{
    while (!(UCSR0A & (1<<UDRE0))){}                             
    UDR0 = c;
    return 0;
}

void uart_puts (char *s)
{
  while (*s)
  {
    uart_putc(*s);
    s++;
  }
}

ISR(TIMER1_CAPT_vect)			//Misst die HIGH Pulszeiten, IR invertiert ja
{
  if(bit_is_set(TCCR1B,ICES1))  //steigende flanke
  {
    //alteZeit = ICR1;
    clrbit(TCCR1B,ICES1);		// zurücksetzten auf fallende flanke
    TCNT1=0;
      
  }else							//fallende flanke
  {
    pulsweite = ICR1;
    setbit(TCCR1B,ICES1);		// zurücksetzen auf steigende flanke
      
    pulsweite_array[bitZahl]=pulsweite;
    daten_verarbeiten = 1;

  }
}

void decode(int puls){

  if(bitZahl==1 && (puls<0 || puls>800)){	//Fehlerhaftes Signal, Startsequenz durch Fremdsignal ausgelöst
    uart_puts("Fehler!");
    uart_puts("  ");
    startBit=0;
    bitZahl=0;
    IR_Code=0; 
    setbit(TCCR1B,ICES1);					//initial we wait for rising edge
  }

  //erster 9ms HIGH wird Übersprungen..starte bei LOW
  if (puls>1050 && puls<1200 && (bitZahl==0)){
    uart_puts("Uebertragung start: ");
    IR_Code=0;
    startBit=1;
    bitZahl++;
  }

  if (puls>0 && puls<380 && (startBit==1)){		//Logische 0
    IR_Code=IR_Code<<1;							//0 einschieben
    bitZahl++;
    uart_puts("0");
  }

  if (puls>380 && puls<600 && (startBit==1)){	//Logische 1
    IR_Code=IR_Code<<1;
    IR_Code|=1;									// invertieren 0 einschieben, alles invertieren->1 einschieben
    bitZahl++;
    uart_puts("1");
  }
  
  if (bitZahl==24){ 
	  
	uart_puts(", Hex: ");
    char hex[32];
	itoa(IR_Code, hex, 16);
    uart_puts(hex);	

    uart_puts(", Fertig!\n");
    startBit=0;
    bitZahl=0;
	knopf_druck = 1;
  }

}

ISR(TIMER0_COMPA_vect) {
	counter += 1;
	char counter_string[32];
	itoa(counter, counter_string, 10);
	uart_puts("Counter: ");
	uart_puts(counter_string);
	uart_puts("\n");
	if (counter >= 200) {

		counter = 0;		//reset counter
		TCCR0B = 0;			//timer0 ausschalten
		switch (IR_Code) {
			
			case IR_BUTTON_forward: {			
				//stop motors
				PORTD &= ~( 1 << PD6 );
				PORTD &= ~( 1 << PD5 );
				IR_Code = 0;
			}
			case IR_BUTTON_backward:{
				//stop motors
				PORTD &= ~( 1 << PD7 );
				PORTD &= ~( 1 << PD4 );
				IR_Code = 0;
			}
			case IR_BUTTON_forward_left:{
				//stop motors
				PORTD &= ~( 1 << PD5 );
				IR_Code = 0;
			}
			case IR_BUTTON_forward_right:{
				//stop motors
				PORTD &= ~( 1 << PD6 );	
				IR_Code = 0;
			}
			case IR_BUTTON_backward_left:{
			    //stop motors
			    PORTD &= ~( 1 << PD4 );	
				IR_Code = 0;		
			}
			case IR_BUTTON_backward_right:{
			    //stop motors
			    PORTD &= ~( 1 << PD7 );	
				IR_Code = 0;		
			}
		}
	}
}	

int main()
{
  //UART INIT
  UBRR0H = 0;
  UBRR0L = 25; //38.4k
  UCSR0C = 0b00000110; //8-Data, 1 stop
  UCSR0B = (1<<TXEN0);

  //TIMER INIT
  TCCR1B = (1<<CS11)|(1<<CS10)|(1<<ICES1)|(1<<ICNC1);	// prescalar 64, ICP initial interrupt on rising edge
  TIMSK1 = (1<<ICIE1);									// enable icp1 interrupt

  clrbit(DDRB,ICP_PIN);									// input
  
  //motors setup
  DDRD = (1<<PD7); // right motors; motor A
  DDRD = (1<<PD6); // right motors; motor A
  DDRD = (1<<PD5); // left motors; motor B
  DDRD = (1<<PD4); // left motors; motor B
  PORTD = 0;  
  
  counter = 0;
  
  sei();

  while(1)
  {
	if(knopf_druck){
	  //timer0 setup
	  TCCR0A = (1 << WGM01);					//ctc modus with top OCRA
	  TIMSK0 = (1 << OCIE0A);					// enable interrupt 0A
	  //TCCR0B = (1 << CS02) | (1 << CS00);		//1024 prescaling
	  OCR0A = 15;	
	
	  knopf_druck = 0;  
	}
	  
    if(daten_verarbeiten)
    {
		cli();
		decode(pulsweite_array[bitZahl]);	//pulszeit = pulsweite; // pulsezeit in ms
	
		sei();
		daten_verarbeiten = 0;    
    }
	
    switch (IR_Code) {	
		
	    case IR_BUTTON_forward: {
			
			if (counter<=5){uart_puts("Pressed on button 2");}

			TCCR0B = (1 << CS02) | (1 << CS00);   //timer0 power on
			TCNT0=0;
			if(IR_Code!=0){
				//right motors A
				PORTD |= ( 1 << PD6 );
				PORTD &= ~( 1 << PD7 );
				//left motors B
				PORTD |= ( 1 << PD5 );
				PORTD &= ~( 1 << PD4 );
				//delay(500);
			}
			break;
	    }
	    case IR_BUTTON_backward: {
		    if (counter<=5){uart_puts("Pressed on button 8");}
		    
			TCCR0B = (1 << CS02) | (1 << CS00);   //timer0 power on
			TCNT0=0;
			if(IR_Code!=0){
				//right motors A
				PORTD |= ( 1 << PD7 );
				PORTD &= ~( 1 << PD6 );
				//left motors B
				PORTD |= ( 1 << PD4 );
				PORTD &= ~( 1 << PD5 );		
			}
		    break;
	    }
	    case IR_BUTTON_forward_left: {
		    if (counter<=5){uart_puts("Pressed on button 3");}
		    
			TCCR0B = (1 << CS02) | (1 << CS00);
			TCNT0=0;
			if(IR_Code!=0){	
				//right motors A -> do nothing -> right curve	
				PORTD &= ~( 1 << PD6 );
				PORTD &= ~( 1 << PD7 );
				//left motors B
				PORTD |= ( 1 << PD5 );
				PORTD &= ~( 1 << PD4 );
			}
		    break;
	    }
	    case IR_BUTTON_forward_right: {
		    if (counter<=5){uart_puts("Pressed on button 1");}
			TCCR0B = (1 << CS02) | (1 << CS00);
			TCNT0=0;
			if(IR_Code!=0){			
				//right motors A
				PORTD |= ( 1 << PD6 );
				PORTD &= ~( 1 << PD7 );
				//left motors B -> do nothing -> left curve
				PORTD &= ~( 1 << PD5 );
				PORTD &= ~( 1 << PD4 );
			}
		    break;
	    }
	    case IR_BUTTON_backward_left: {
		    if (counter<=5){uart_puts("Pressed on button 9");}
			TCCR0B = (1 << CS02) | (1 << CS00);
			TCNT0=0;
			if(IR_Code!=0){		
				//right motors A -> do nothing -> right curve
				PORTD &= ~( 1 << PD6 );
				PORTD &= ~( 1 << PD7 );
				//left motors B
				PORTD |= ( 1 << PD4 );
				PORTD &= ~( 1 << PD5 );
			}
		    break;
	    }
	    case IR_BUTTON_backward_right: {
		    if (counter<=5){uart_puts("Pressed on button 7");}
			TCCR0B = (1 << CS02) | (1 << CS00);
			TCNT0=0;
			if(IR_Code!=0){			
				//right motors A
				PORTD |= ( 1 << PD7 );
				PORTD &= ~( 1 << PD6 );
				//left motors B -> do nothing -> left curve
				PORTD &= ~( 1 << PD5 );
				PORTD &= ~( 1 << PD4 );
			}
		    break;
	    }		
	    default: {
		    uart_puts("Button not recognized");
	    }
    }	
  } 
}
