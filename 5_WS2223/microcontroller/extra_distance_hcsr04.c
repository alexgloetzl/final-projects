// Additionally to the IR remote controlled car
// a distance measuring device HC-SR04 was also implemented
// in C. However with only one ICP (Input Capture Pin)
// on the Arduino I could not manage to merge this script
// with the main robot car program successfully.

// The distance measuring of the HC-SR04 starts by setting the TRIGGER pin to HIGH for 10 micro seconds. This sends out an ultrasonic 
// sound wave. After the wave is transmitted the ECHO pin is automatically set to HIGH and "waits" now for the echo of the wave to
// be reflected back. As soon as the reflection reaches the sensor the ECHO pin is set to LOW. Therefore the length of the ECHO 
// pulse gives an estimate of how far away the obstacle is located.


#ifndef __AVR_ATmega328P__
#define __AVR_ATmega328P__
#endif

#define F_CPU 16000000UL

#include <avr/io.h>
#include <avr/interrupt.h>
#include <stdlib.h>
#include <stdio.h>

#define setbit(port,bit)  ((port) |=  (1<<bit))
#define clrbit(port,bit)  ((port) &= ~(1<<bit))
#define bit_is_set(sfr,bit)  (_SFR_BYTE(sfr) & _BV(bit))

//flags
volatile uint32_t timer2_finished = 0;
volatile uint32_t echo_pulsewidth_finished = 0;

void usart_setup(void) {
	UBRR0L = 103;                          // baud rate 9600
	UCSR0B = (1 << TXEN0) | (1 << RXEN0);  // enable transmit and receive
}

void serprintchar(char c) {
	// wait until USART is ready
	while ((UCSR0A & (1 << UDRE0)) == 0) {
	};

	// send char
	UDR0 = c;
}

void serprint(const char* s) {
	int i = 0;
	while (1) {
		char c = s[i];
		if (c == 0) break;  // end of string
		serprintchar(c);
		i++;
	}
}

ISR(TIMER2_COMPA_vect){
	//timer2: prescaler 8 -> 2 cycles per 1 micro second ->
	//	-> with OCR2A set to 20 this gives 10 micro seconds exactly.
	
	TCNT2 = 0;
	while(1){
		if(bit_is_set(TIFR2,OCF2A)){
			clrbit(PORTB, PB1);		//set trigger to LOW after 10 us
			TCCR2B = 0;				//stop timer2
			setbit(TIFR2,OCF2A);	//clear OCF2 flag by setting it to HIGH (see documentation)
			timer2_finished = 1;
			break;
		}
	}
}

uint32_t echo_pulsewidth(){
	uint32_t tic = 0;
	uint32_t toc = 0;
	uint32_t echo_pulsewidth_result = 0;
	
	TCCR1A = 0;				//set timer 1 to normal mode
	TCCR1B = 0b11000101;	//set prescaler to 1024; rising edge detection (for echo pulse); turn noise cancellation on

	while(1){

		if(bit_is_set(TIFR1,ICF1)){  //wait for rising edge of echo
			tic = ICR1L;			 //start measuring the width of echo_pulse: store lower register of ICR1 to tic
			setbit(TIFR1,ICF1);		 //clear ICF1 flag
			TCCR1B = 0b10000101;	 //enable falling edge detection

			break;
		}
	}
	while(1){
		if(bit_is_set(TIFR1,ICF1)){
			toc = ICR1L;			//stop measuring pulse width and store value
			setbit(TIFR1,ICF1);     //clear ICF1 flag
			echo_pulsewidth_finished = 1;

			echo_pulsewidth_result = toc-tic;
			return echo_pulsewidth_result;	
		}	
	}
}

int main()
{
	usart_setup();	
	
	setbit(DDRB,PB1); //trigger is output
	clrbit(DDRB,PB0);  //echo is input
	
	//timer2 init
	TCCR2A = 0b00000010;
	TCCR2B = 0; //timer2 off
	TIMSK2 = 0b00000010;
	OCR2A = 20;			//we want (at least) 10 micro seconds (OCR2A = 20) of HIGH on the trigger.

	sei();
	
	while(1){
		clrbit(PORTB, PB1);
		setbit(PORTB, PB1);		//set trigger to HIGH for 10 micro seconds
		TCCR2B = 0b00000010;	//enable timer2, prescaler 8, CTC mode

		while(1){
			if(timer2_finished == 1){			//wait for 10us trigger pulse to finish
				timer2_finished = 0;
				uint32_t echo_result = echo_pulsewidth();
				serprintuint16(echo_result);

				break;
			}				
		}

		
		if(echo_pulsewidth_finished == 1){    //wait for echo pulse width measurement to finish		
			echo_pulsewidth_finished = 0;
			uint32_t counter3 = 0;			//delay function: need small delay after echo measurement according to documentation
			for (uint32_t z=0; z<(300000); ++z){
				counter3++;
			}
		}
	}
}