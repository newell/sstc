# sstc
This project is my designe of a half-bridge Solid State Tesla Coil (SSTC).

An SSTC is a type of [Tesla coil](https://en.wikipedia.org/wiki/Tesla_coil) that uses modern semiconductor devices such as MOSFETs or IGBTs to generate high-frequency alternating current (AC) and high voltages. The term "half-bridge" refers to the specific configuration of the power electronics used in the coil.

## How Half-Bridge SSTCs Work

1. **Power Supply**: The primary coil is powered by a DC power supply. This DC voltage is then switched on and off at a high frequency by the half-bridge circuit.

2. **Half-Bridge Configuration**:
   - **Half-Bridge Circuit**: The half-bridge circuit consists of two semiconductor switches (typically MOSFETs or IGBTs) and two capacitors. One switch is connected to the positive rail of the power supply, and the other switch is connected to the negative rail. The junction between the two switches connects to one end of the primary coil.
   - **Switching**: The switches are controlled in such a way that they turn on and off alternately. When one switch is on, it allows current to flow through the primary coil in one direction, and when the other switch is on, it allows current to flow in the opposite direction. This creates an alternating current (AC) in the primary coil.

3. **Resonant Circuit**: The primary coil and the primary capacitor form a resonant circuit. The switching frequency of the half-bridge circuit is typically set to match the resonant frequency of this LC circuit, which maximizes the energy transfer to the secondary coil.

4. **Secondary Coil**: The secondary coil, which is coupled to the primary coil via magnetic induction, has many more turns than the primary coil. This step-up transformer action increases the voltage to very high levels.

5. **Top Load**: The top load (usually a toroid) of the secondary coil helps to shape the electric field and allows the coil to produce long electrical discharges (sparks).

### Why It’s Called "Half-Bridge"

The term "half-bridge" comes from the structure of the circuit:
- **Full-Bridge vs. Half-Bridge**: In a full-bridge circuit, there are four switches arranged in an H-bridge configuration. This allows for full control over the direction of the current through the load (primary coil). In contrast, a half-bridge circuit uses only two switches and two capacitors. It controls the current direction by alternately switching the two switches, but only half of the H-bridge is implemented.
- **Simplified Design**: The half-bridge design is simpler and more cost-effective compared to a full-bridge design, making it a popular choice for SSTCs.


