import torch
from gammalearn.utils import compute_dann_hparams


# TODO fix gradnorm for lightning
# see manual optimization in lightning doc
# def training_step_gradnorm(module, batch):
#     """
#     The training operations for one batch for vanilla mt learning
#     Parameters
#     ----------
#     module: LightningModule
#     batch
#
#     Returns
#     -------
#
#     """
#     # Load data
#     images = batch['image']
#     labels = batch['label']
#
#     output = module.net(images)
#
#     # Compute loss
#     losses, loss_data = module.experiment.compute_loss(output, labels)
#     losses = torch.stack(losses)
#     weighted_losses = losses * module.experiment.compute_loss.weights
#     loss = torch.sum(weighted_losses)
#
#     # Compute gradients w.r.t. the parameters of the network
#     loss.backward(retain_graph=True)
#
#     module.experiment.compute_loss.zero_grad()
#
#     # Compute the inverse training rate
#     loss_ratio = losses / module.experiment.compute_loss.initial_losses.to(module.experiment.device)
#     average_loss_ratio = loss_ratio.mean()
#     inverse_training_rate = loss_ratio / average_loss_ratio
#
#     # Compute the gradient norm of each task and the mean gradient norm
#     gw_norms = []
#     if hasattr(module.net, 'feature'):
#         common_layer = getattr(module.net.feature, module.experiment.compute_loss.last_common_layer)
#     else:
#         common_layer = getattr(module.net, module.experiment.compute_loss.last_common_layer)
#     for i, loss in enumerate(losses):
#         gw = torch.autograd.grad(loss,
#                                  common_layer.parameters(),
#                                  retain_graph=True)[0]
#         gw_norms.append(torch.norm(gw * module.experiment.compute_loss.weights[i]))
#     gw_mean = torch.stack(gw_norms).mean().to(module.experiment.device)
#
#     # Gradient target (considered as a constant term)
#     grad_target = gw_mean * (inverse_training_rate**module.experiment.compute_loss.alpha)
#     grad_target = grad_target.clone().detach().requires_grad_(False)
#     # Gradnorm loss
#     gradnorm_loss = torch.sum(torch.abs(torch.stack(gw_norms).to(module.experiment.device) - grad_target))
#
#     module.experiment.compute_loss.weights.grad = torch.autograd.grad(gradnorm_loss,
#                                                                       module.experiment.compute_loss.weights)[0]
#
#     for _, optim in experiment.optimizers.items():
#         if optim is not None:
#             optim.step()
#
#     # Normalize gradient weights
#     module.experiment.compute_loss.weights.data = module.experiment.compute_loss.weights * (module.experiment.compute_loss.task_number /
#                                                                               module.experiment.compute_loss.weights.sum())
#
#     return output, labels, loss_data


def training_step_mt(module, batch):
    """
    The training operations for one batch for vanilla mt learning
    Parameters
    ----------
    module: LightningModule
    batch

    Returns
    -------

    """
    # Load data
    images = batch['image']
    labels = batch['label']

    output = module.net(images)

    # Compute loss
    loss, loss_data = module.experiment.compute_loss(output, labels)
    loss = torch.stack(loss).sum()
    if module.experiment.regularization is not None:
        loss += module.experiment.regularization['function'](module.net) * module.experiment.regularization['weight']

    return output, labels, loss_data, loss


def training_step_ae(module, batch):
    """
    The training operations for one batch for autoencoder
    Parameters
    ----------
    module: LightningModule
    batch

    Returns
    -------

    """
    # Load data
    images = batch['image']

    output = module.net(images)

    # Compute loss
    loss = module.experiment.compute_loss(output, images)

    if module.experiment.regularization is not None:
        loss += module.experiment.regularization['function'](module.net) * module.experiment.regularization['weight']

    loss = loss.mean()

    return None, None, {'autoencoder': loss.detach().item()}, loss


def training_step_dann(module, batch): # TO DO
    """
    The training operations for one batch for vanilla mt learning
    Parameters
    ----------
    module: LightningModule
    batch

    Returns
    -------

    """
    # Load data
    images_source = batch['image_source']
    images_target = batch['image_target']
    labels_source = batch['label_source']

    output_source = module.net(images_source)
    output_target = module.net(images_target)

    source_domain_class = output_source.pop('domain_class')
    target_domain_class = output_target['domain_class']

    lambda_p, _ = compute_dann_hparams(module)

    # Compute loss
    loss_rec_phys, loss_data = module.experiment.compute_loss(output_source, labels_source)
    loss_rec_phys = torch.stack(loss_rec_phys).sum() 

    domain_label_source = torch.full((len(source_domain_class),), fill_value=1, device=source_domain_class.device)
    domain_label_target = torch.full((len(target_domain_class),), fill_value=0, device=target_domain_class.device)

    domain_class = torch.cat([source_domain_class, target_domain_class])
    domain_label = torch.cat([domain_label_source, domain_label_target])

    loss_domain_class = torch.nn.CrossEntropyLoss()(domain_class, domain_label)
    loss = loss_rec_phys + loss_domain_class * lambda_p

    loss_data['domain_class'] = loss_domain_class.detach().item()

    if module.experiment.regularization is not None:
        loss += module.experiment.regularization['function'](module.net) * module.experiment.regularization['weight']

    output_source['domain_class'] = domain_class
    labels_source['domain_class'] = domain_label
    
    return output_source, labels_source, loss_data, loss


def training_step_mt_gradient_penalty(module, batch):
    """
    The training operations for one batch for vanilla mt learning with gradient penalty
    Parameters
    ----------
    module: LightningModule
    batch
        Returns
        -------

        """

        # Load data
    images = batch['image']
    labels = batch['label']

    images.requires_grad = True

    output = module.net(images)

    # Compute loss
    loss, loss_data = module.experiment.compute_loss(output, labels)
    loss = torch.stack(loss).sum()
    if module.experiment.regularization is not None:
        gradient_x = torch.autograd.grad(loss, images, retain_graph=True)[0]
        penalty = torch.mean((torch.norm(gradient_x.view(gradient_x.shape[0], -1), 2, dim=1) - 1) ** 2)
        loss += penalty * module.experiment.regularization['weight']

    return output, labels, loss_data, loss


def eval_step_mt(module, batch):
    """
    The validating operations for one batch
    Parameters
    ----------
    module
    batch

    Returns
    -------

    """
    images = batch['image']
    labels = batch['label']

    output = module.net(images)
    # Compute loss and quality measures
    loss, loss_data = module.experiment.compute_loss(output, labels)
    loss = torch.stack(loss).sum()

    return output, labels, loss_data, loss


def eval_step_ae(module, batch):
    """
    The training operations for one batch for autoencoder
    Parameters
    ----------
    module: LightningModule
    batch

    Returns
    -------

    """
    # Load data
    images = batch['image']

    output = module.net(images)

    # Compute loss
    loss = module.experiment.compute_loss(output, images)
    loss = loss.mean()

    return None, None, {'autoencoder': loss.detach().item()}, loss


def eval_step_dann(module, batch):
    # Load data
    images_source = batch['image_source']
    images_target = batch['image_target']
    labels_source = batch['label_source']

    output_source = module.net(images_source)
    output_target = module.net(images_target)

    source_domain_class = output_source.pop('domain_class')
    target_domain_class = output_target['domain_class']

    lambda_p, _ = compute_dann_hparams(module)

    # Compute loss
    loss_rec_phys, loss_data = module.experiment.compute_loss(output_source, labels_source)
    loss_rec_phys = torch.stack(loss_rec_phys).sum() 

    domain_label_source = torch.full((len(source_domain_class),), fill_value=1, device=source_domain_class.device)
    domain_label_target = torch.full((len(target_domain_class),), fill_value=0, device=target_domain_class.device)

    domain_class = torch.cat([source_domain_class, target_domain_class])
    domain_label = torch.cat([domain_label_source, domain_label_target])

    loss_domain_class = torch.nn.CrossEntropyLoss()(domain_class, domain_label)
    loss = loss_rec_phys + loss_domain_class * lambda_p

    loss_data['domain_class'] = loss_domain_class.detach().item()
    output_source['domain_class'] = domain_class
    labels_source['domain_class'] = domain_label

    return output_source, labels_source, loss_data, loss


def test_step_mt(module, batch):
    """
    The validating operations for one batch
    Parameters
    ----------
    module
    batch

    Returns
    -------

    """
    images = batch['image']

    output = module.net(images)

    return output, batch['dl1_params']


def test_step_ae(module, batch):
    """
    The validating operations for one batch
    Parameters
    ----------
    module
    batch

    Returns
    -------

    """
    images = batch['image']

    output = module.net(images)

    # Compute loss
    loss = module.experiment.compute_loss(output, images)
    # We reduce the loss per image
    loss = torch.mean(loss, dim=tuple(torch.arange(loss.dim())[1:]))

    return {'ae_error': loss.detach()}, batch['dl1_params']


def test_step_dann(module, batch):
    """
    The validating operations for one batch
    Parameters
    ----------
    module
    batch

    Returns
    -------

    """
    # Load data
    images_source = batch['image']

    output_source = module.net(images_source)

    return output_source, batch['dl1_params']