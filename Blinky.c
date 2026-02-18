/*---------------------------------------------------------------------------
 * Copyright (c) 2024 Arm Limited (or its affiliates).
 * All rights reserved.
 *
 * SPDX-License-Identifier: Apache-2.0
 *
 * Licensed under the Apache License, Version 2.0 (the License); you may
 * not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an AS IS BASIS, WITHOUT
 * WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 *---------------------------------------------------------------------------*/

#include <stdio.h>

#include "main.h"

#include "cmsis_os2.h"                  // ::CMSIS:RTOS2
#include "cmsis_vio.h"
#include "rl_net.h"                     // Keil::Network&MDK:CORE

static osThreadId_t tid_thrLED;         // Thread id of thread: LED
static osThreadId_t tid_thrButton;      // Thread id of thread: Button

bool LEDrun;

static uint32_t analog_val;

/* Read analog inputs */
int32_t analog_in (uint32_t ch) {
  int32_t val = 0;

  if (ch == 3) {
		HAL_ADC_Start(&hadc3);
		HAL_ADC_PollForConversion(&hadc3, HAL_MAX_DELAY);
		val = HAL_ADC_GetValue(&hadc3);
		HAL_ADC_Stop(&hadc3);
  } else if (ch == 0) {
		val = analog_val & 0x3FF;
	}
  return (val);
}

/*-----------------------------------------------------------------------------
  thrLED: blink LED
 *----------------------------------------------------------------------------*/
static __NO_RETURN void thrLED (void *argument) {
  uint32_t active_flag = 0U;
  uint32_t led1_state = 0U;

  (void)argument;

  for (;;) {
    if (osThreadFlagsWait(1U, osFlagsWaitAny, 0U) == 1U) {
      active_flag ^= 1U;
    }

//    if (active_flag == 1U) {
//      //toggle vioLED1
//      led1_state ^= 1U;                         // Toggle LED1 state
//      vioSetSignal(vioLED1, led1_state ? vioLEDon : vioLEDoff);
//    }

//    if (LEDrun == true) {
//      vioSetSignal(vioLED0, vioLEDon);          // Switch LED0 on
//      osDelay(500U);                            // Delay 500 ms
//      vioSetSignal(vioLED0, vioLEDoff);         // Switch LED0 off
//      osDelay(500U);                            // Delay 500 ms
//    }

    osDelay(500U);
    analog_val += 10;

  }
}

/*-----------------------------------------------------------------------------
  thrButton: check Button state
 *----------------------------------------------------------------------------*/
static __NO_RETURN void thrButton (void *argument) {
  uint32_t last = 0U;
  uint32_t state;

  (void)argument;

  for (;;) {
    state = (vioGetSignal(vioBUTTON0));           // Get pressed Button state
    if (state != last) {
      if (state == 1U) {
        osThreadFlagsSet(tid_thrLED, 1U);         // Set flag to thrLED
      }
      last = state;
    }
    osDelay(100U);
  }
}

/*-----------------------------------------------------------------------------
 * Application main thread
 *----------------------------------------------------------------------------*/
/* IP address change notification */
void netDHCP_Notify (uint32_t if_id, uint8_t option, const uint8_t *val, uint32_t len) {
  char ip_ascii[16];
  (void)len;

  if ((if_id == (NET_IF_CLASS_ETH | 0)) && (option == NET_DHCP_OPTION_IP_ADDRESS)) {
    netIP_ntoa (NET_ADDR_IP4, val, ip_ascii, sizeof(ip_ascii));
    printf("IP4: %s\n",ip_ascii);
  }
}

__NO_RETURN void app_main_thread (void *argument) {
	(void)argument;
	uint8_t ip_addr[NET_ADDR_IP6_LEN];
  char    ip_ascii[40];

  printf("Blinky example\n");

  tid_thrLED = osThreadNew(thrLED, NULL, NULL);         // Create LED thread
  tid_thrButton = osThreadNew(thrButton, NULL, NULL);   // Create Button thread
	
	netInitialize ();
	
	printf("IP4: Waiting for DHCP\n");
  if (netIF_GetOption(NET_IF_CLASS_ETH | 0,
                      netIF_OptionIP6_LinkLocalAddress,
                      ip_addr, sizeof(ip_addr)) == netOK) {
    /* IPv6 enabled on ETH0, print Link-local address */
    netIP_ntoa(NET_ADDR_IP6, ip_addr, ip_ascii, sizeof(ip_ascii));
    printf("IP6: %s\n", ip_ascii);
	}
	
	osThreadExit();
	
  for (;;) {                            // Loop forever
  }
}

/*-----------------------------------------------------------------------------
 * Application initialization
 *----------------------------------------------------------------------------*/
int Init_GUIThread (void);

int app_main (void) {
  osKernelInitialize();                         /* Initialize CMSIS-RTOS2 */
  osThreadNew(app_main_thread, NULL, NULL);
	Init_GUIThread();
  osKernelStart();                              /* Start thread execution */
  return 0;
}
