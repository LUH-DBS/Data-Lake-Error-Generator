/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package it.unibas.bartgui.view.panel.editor.Dependency;

import it.unibas.bartgui.resources.R;
import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Dimension;
import org.jdesktop.swingx.JXLabel;
import org.openide.util.ImageUtilities;
import org.pushingpixels.trident.Timeline;
import org.pushingpixels.trident.ease.Spline;

/**
 *
 * @author Grandinetti Giovanni <grandinetti.giovanni13@gmail.com>
 */
public class DependecyWPanel extends javax.swing.JPanel {

    
    /**
     * Creates new form DependecyWPanel
     */
    
    private JXLabel labelDependency;
    private Timeline animate;
    private Timeline fadeInTimeline; 
    private int red = 204, green = 207, blu = 213;
    public DependecyWPanel() {
        initComponents();
        initJXLabelDependency(); 
        this.jPanelLabelDependecy.setLayout(new BorderLayout());
        this.jPanelLabelDependecy.add(labelDependency,BorderLayout.CENTER);
        
    }
    
    
    private void initJXLabelDependency()   {
        fadeInTimeline = new Timeline(this); 
        labelDependency = new JXLabel();
        labelDependency.setOpaque(true);
        labelDependency.setMinimumSize(new Dimension(589, 200));
        labelDependency.setPreferredSize(new Dimension(589, 200));
        labelDependency.setLineWrap(false);
        labelDependency.setTextAlignment(JXLabel.TextAlignment.JUSTIFY);       
        labelDependency.setIcon(ImageUtilities.image2Icon(ImageUtilities.loadImage(R.IMAGE_NODE_DCS)));
        labelDependency.setIconTextGap(20);
    }
    
    public void setTextLabelDependency(String text)   {
        labelDependency.setText(text);
    }
    
    
    public void setBackgroundLabelD(int alpha)   {             
        if(red+alpha <= 244)red = red+alpha;
        if(green+alpha <= 250)green = green+alpha;
        if(blu+alpha <= 250)blu = blu+alpha;
        labelDependency.setBackground(new Color(red, green, blu));
    }

    
    public synchronized void animateBackground()   { 
        fadeInTimeline.addPropertyToInterpolate("backgroundLabelD",  0 , 55); 
        fadeInTimeline.setDuration(1500); 
        fadeInTimeline.setEase(new Spline(0.7f)); 
        fadeInTimeline.play(); 
        //fadeInTimeline.playLoop(2, Timeline.RepeatBehavior.LOOP);
    }
    /**
     * This method is called from within the constructor to initialize the form.
     * WARNING: Do NOT modify this code. The content of this method is always
     * regenerated by the Form Editor.
     */
    @SuppressWarnings("unchecked")
    // <editor-fold defaultstate="collapsed" desc="Generated Code">//GEN-BEGIN:initComponents
    private void initComponents() {

        jPanelLabelDependecy = new javax.swing.JPanel();

        setBorder(javax.swing.BorderFactory.createBevelBorder(javax.swing.border.BevelBorder.RAISED));
        setMinimumSize(new java.awt.Dimension(613, 225));
        setPreferredSize(new java.awt.Dimension(613, 225));

        jPanelLabelDependecy.setBorder(javax.swing.BorderFactory.createTitledBorder(new javax.swing.border.SoftBevelBorder(javax.swing.border.BevelBorder.LOWERED), org.openide.util.NbBundle.getMessage(DependecyWPanel.class, "DependecyWPanel.jPanelLabelDependecy.border.title"), javax.swing.border.TitledBorder.CENTER, javax.swing.border.TitledBorder.TOP, new java.awt.Font("Tahoma", 0, 11), new java.awt.Color(0, 51, 204))); // NOI18N
        jPanelLabelDependecy.setMinimumSize(new java.awt.Dimension(589, 178));
        jPanelLabelDependecy.setPreferredSize(new java.awt.Dimension(589, 178));

        javax.swing.GroupLayout jPanelLabelDependecyLayout = new javax.swing.GroupLayout(jPanelLabelDependecy);
        jPanelLabelDependecy.setLayout(jPanelLabelDependecyLayout);
        jPanelLabelDependecyLayout.setHorizontalGroup(
            jPanelLabelDependecyLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGap(0, 575, Short.MAX_VALUE)
        );
        jPanelLabelDependecyLayout.setVerticalGroup(
            jPanelLabelDependecyLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGap(0, 168, Short.MAX_VALUE)
        );

        javax.swing.GroupLayout layout = new javax.swing.GroupLayout(this);
        this.setLayout(layout);
        layout.setHorizontalGroup(
            layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(layout.createSequentialGroup()
                .addContainerGap()
                .addComponent(jPanelLabelDependecy, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                .addContainerGap())
        );
        layout.setVerticalGroup(
            layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(layout.createSequentialGroup()
                .addContainerGap()
                .addComponent(jPanelLabelDependecy, javax.swing.GroupLayout.PREFERRED_SIZE, 191, javax.swing.GroupLayout.PREFERRED_SIZE)
                .addContainerGap(19, Short.MAX_VALUE))
        );
    }// </editor-fold>//GEN-END:initComponents


    // Variables declaration - do not modify//GEN-BEGIN:variables
    private javax.swing.JPanel jPanelLabelDependecy;
    // End of variables declaration//GEN-END:variables
}
