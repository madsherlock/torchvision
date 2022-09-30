import torch
from torchvision.prototype import features


def test_isinstance():
    assert isinstance(
        features.Label([0, 1, 0], categories=["foo", "bar"]),
        torch.Tensor,
    )


def test_wrapping_no_copy():
    tensor = torch.tensor([0, 1, 0], dtype=torch.int64)
    label = features.Label(tensor, categories=["foo", "bar"])

    assert label.data_ptr() == tensor.data_ptr()


def test_to_wrapping():
    tensor = torch.tensor([0, 1, 0], dtype=torch.int64)
    label = features.Label(tensor, categories=["foo", "bar"])

    label_to = label.to(torch.int32)

    assert type(label_to) is features.Label
    assert label_to.dtype is torch.int32
    assert label_to.categories is label.categories


def test_to_feature_reference():
    tensor = torch.tensor([0, 1, 0], dtype=torch.int64)
    label = features.Label(tensor, categories=["foo", "bar"]).to(torch.int32)

    tensor_to = tensor.to(label)

    assert type(tensor_to) is torch.Tensor
    assert tensor_to.dtype is torch.int32


def test_clone_wrapping():
    tensor = torch.tensor([0, 1, 0], dtype=torch.int64)
    label = features.Label(tensor, categories=["foo", "bar"])

    label_clone = label.clone()

    assert type(label_clone) is features.Label
    assert label_clone.data_ptr() != label.data_ptr()
    assert label_clone.categories is label.categories


def test_other_op_no_wrapping():
    tensor = torch.tensor([0, 1, 0], dtype=torch.int64)
    label = features.Label(tensor, categories=["foo", "bar"])

    # any operation besides .to() and .clone() will do here
    output = label * 2

    assert type(output) is torch.Tensor


def test_new_like():
    tensor = torch.tensor([0, 1, 0], dtype=torch.int64)
    label = features.Label(tensor, categories=["foo", "bar"])

    # any operation besides .to() and .clone() will do here
    output = label * 2

    label_new = features.Label.new_like(label, output)

    assert type(label_new) is features.Label
    assert label_new.data_ptr() == output.data_ptr()
    assert label_new.categories is label.categories